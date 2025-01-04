Real-Time Deepfake Detection
Overview
The Real-Time Deepfake Detection project is a software application that leverages advanced AI techniques to detect whether a given video is real or deepfake. It analyzes the content with a confidence score and provides segment-by-segment detection for live streams. Additionally, when the confidence level exceeds 90%, the results and associated videos are securely stored in a blockchain for integrity and transparency.

Features
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


**MODELS USED**
Ensure that the models provided in the below link is downloaded and stored locally in the project folder
Keras Model
https://drive.google.com/file/d/1w3Dbhh7DAwS3Tf-w2Td7cq1NXQBITmvo/view?usp=drive_link

Quantised model link
https://drive.google.com/file/d/1y5xwv8swN6m12PKi-RD0SqII2SA6JhpS/view?usp=sharing
