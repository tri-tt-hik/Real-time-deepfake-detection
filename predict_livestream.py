import json
import cv2
import yt_dlp
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from urllib.parse import urlparse, parse_qs

stop_streaming=False

def get_embed_url(youtube_url):
    """Generate the embeddable YouTube URL."""
    parsed_url = urlparse(youtube_url)
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get('v', [None])[0]
    elif parsed_url.hostname == 'youtu.be':
        video_id = parsed_url.path.lstrip('/')
    else:
        return None

    if video_id:
        return f"https://www.youtube.com/embed/{video_id}"
    return None

def get_youtube_stream_url(youtube_url):
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': True,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        return info['url']

# Display the frame using Matplotlib
def show_frame_with_matplotlib(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB for Matplotlib
    plt.imshow(frame_rgb)
    plt.axis('off')  # Hide axes
    plt.pause(0.001) 

interpreter = tf.lite.Interpreter(model_path="det_model/quantised_model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()  

# Constants
TIMESTEPS = 10  # Number of frames per segment
FRAME_HEIGHT = 128
FRAME_WIDTH = 128
FRAME_CHANNELS = 3

def process_video_segment(segment):
    """Run inference on a segment of video frames."""
    # Ensure segment shape: [1, 10, 128, 128, 3]
    segment = np.expand_dims(segment, axis=0).astype(np.float32)
    
    # Set tensor and invoke the model
    interpreter.set_tensor(input_details[0]['index'], segment)
    interpreter.invoke()
    
    # Get predictions
    output_data = interpreter.get_tensor(output_details[0]['index'])
    label_idx = np.argmax(output_data)
    confidence = output_data[0][label_idx]
    
    return "Deepfake" if label_idx == 1 else "Real", confidence

def resize_and_normalize(frame):
    """Resize a frame to model input size and normalize it."""
    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
    frame = frame / 255.0  # Normalize to [0, 1]
    return frame

import time  # Importing time to track elapsed time

def capture_youtube_stream(youtube_url):
    """Capture frames from a YouTube livestream."""
    global stop_streaming
    best_url = get_youtube_stream_url(youtube_url)
    print("best url: ", best_url)
    cap = cv2.VideoCapture(best_url)

    if not cap.isOpened():
        print("Failed to open video stream.")
        return {"error": "Unable to open stream"}

    frame_sec = 1
    frame_buffer = []  # Buffer to store TIMESTEPS frames
    real_weight = 0.0
    fake_weight = 0.0
    result = []
    final_result = []

    while cap.isOpened():
        if stop_streaming:
            print("Streaming stopped by user.")
            break

        ret, frame = cap.read()
        if not ret:
            print("Stream ended or failed.")
            break

        # Resize and normalize frame
        resized_frame = resize_and_normalize(frame)
        frame_buffer.append(resized_frame)

        # If buffer is full, process the segment
        if len(frame_buffer) == TIMESTEPS:
            label, confidence = process_video_segment(np.array(frame_buffer))
            confidence = confidence * 100
            if label == "Real":
                real_weight += confidence
            else:
                fake_weight += confidence

            result.append({
                "Second": frame_sec,
                "final": {"prediction": label, "Confidence": confidence}
            })

            # Save results to file for real-time updates
            with open("current_results.json", "w") as f:
                json.dump({"results": result}, f)

            frame_sec += 1
            frame_buffer = []

    # Final prediction after analysis ends
    final_label = "Real" if real_weight > fake_weight else "Deepfake"
    final_confidence = max(real_weight, fake_weight) / max(frame_sec - 1, 1)
    final_result = {"FinalPrediction": {"label": final_label, "confidence": final_confidence}}

    cap.release()
    print(result)
    print(final_result)
    return [result, final_result]