import tensorflow as tf
import cv2
import numpy as np
import os

# Function to extract frames from the video
def extract_frames(video_path, output_size=(128, 128), frame_count=10):
    cap = cv2.VideoCapture(video_path)
    frames = []
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = max(total_frames // frame_count, 1)
    
    for i in range(frame_count):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * step)
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, output_size)
        frames.append(frame)
    cap.release()
    frames = np.array(frames)
    frames = frames / 255.0  # Normalize the frames

    # Add batch dimension (shape should be [1, frames, height, width, channels])
    return np.expand_dims(frames, axis=0)

# Function to predict if a video is real or fake
def predict_video(video_path):
    model_path = os.path.join("det_model", "quantised_model.tflite")

    # Load the TensorFlow Lite model
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Extract frames from the video
    frames = extract_frames(video_path)

    # Set the input tensor
    interpreter.set_tensor(input_details[0]['index'], frames.astype(np.float32))
    interpreter.invoke()

    # Get the output tensor
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    predicted_class = np.argmax(output_data, axis=1)[0]
    confidence = output_data[0][predicted_class]
    confidence=confidence*100
    label = "FAKE" if predicted_class == 1 else "REAL"
    return {"label": label, "confidence": confidence}
