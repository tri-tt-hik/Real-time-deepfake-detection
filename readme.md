**Real-Time Deepfake Detection**

**Overview**


The Real-Time Deepfake Detection project is a software application that leverages advanced AI techniques to detect whether a given video is real or deepfake. It analyzes the content with a confidence score and provides segment-by-segment detection for live streams. Additionally, when the confidence level exceeds 90%, the results and associated videos are securely stored in a blockchain for integrity and transparency.

**Features**


Video Detection: Upload a video file to analyze and determine whether it is real or a deepfake, along with a confidence score.


Live Stream Detection: Provide a YouTube live stream URL to detect deepfake segments in real-time.
Blockchain Integration: Automatically store video data and detection results in a blockchain if the confidence score exceeds 90%.


User-Friendly Interface: Simple and intuitive interface for both video uploads and live stream URL inputs.
Real-Time Results: Instant detection and confidence score display for live streams and uploaded videos.


Installation
Follow these steps to set up the project locally:

Clone the repository:

bash
Copy code
git clone https://github.com/tri-tt-hik/Real-time-deepfake-detection.git
cd Real-time-deepfake-detection
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Set up the blockchain component:

Configure the blockchain network (details in the blockchain_config directory).
Ensure the blockchain service is running locally or on the designated network.
Run the application:

bash
Copy code
python manage.py runserver
Access the application at http://127.0.0.1:8000 in your browser.

**Usage**

**Video Detection**

1.Navigate to the "Video Detection" section.
2.Upload a video file (supported formats: .mp4, .avi, .mov, etc.).
3.Click "Analyze" to view the detection result and confidence score.


**Live Stream Detection**

1.Navigate to the "Live Stream Detection" section.
2.Paste the YouTube live stream URL.
3.Start the analysis to detect real or deepfake segments in real-time.

**Blockchain Integration**
If the confidence score exceeds 90%, the video and its prediction results are securely stored in the blockchain for future verification and integrity.

**Project Architecture**

**Frontend:** User interface built with HTML, CSS, and JavaScript.
**Backend:** Python/Django for processing and serving requests.
**AI Model:** Deep learning-based model for real-time deepfake detection.
**Blockchain:** Immutable storage of videos and results using a private/public blockchain framework.

**Requirements**

Python 3.8 or higher
Django framework
opencv (for video detection)
TensorFlow or PyTorch (for deepfake detection model)
Blockchain framework (e.g., Ethereum, Hyperledger Fabric, or custom implementation)


**MODELS USED**
Ensure that the models provided in the below link is downloaded and stored locally in the project folder


**Keras Model**

https://drive.google.com/file/d/1w3Dbhh7DAwS3Tf-w2Td7cq1NXQBITmvo/view?usp=drive_link

**Quantised model link**

https://drive.google.com/file/d/1y5xwv8swN6m12PKi-RD0SqII2SA6JhpS/view?usp=sharing
