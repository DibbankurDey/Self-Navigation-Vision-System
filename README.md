# Self-Navigation Vision System

This is an AI-powered Self-Navigation Vision System that utilizes computer vision to assist in real-time navigation. It detects objects using YOLOv8, estimates their distance, determines safe navigational decisions (e.g., steer left, steer right), and provides audible voice warnings and instructions using text-to-speech.

## Features
- **Real-time Object Detection:** Detects pedestrians, vehicles, and other obstacles on the road.
- **Distance Estimation:** Calculates the approximate distance to detected objects.
- **Collision Warning System:** Identifies if an object is dangerously close and issues an alert.
- **Voice Assistant Integration:** Speaks the navigation instructions and collision warnings aloud to the user.
- **Support for Multiple Modes:** Can process static images (`main.py`), pre-recorded videos (`video_navigation.py`), and live camera feeds (`live_navigation.py`).

## Tech Stack
- **Python**
- **OpenCV (`cv2`)** - For image and video processing.
- **Ultralytics (YOLOv8)** - For state-of-the-art object detection.
- **pyttsx3** - For text-to-speech voice assistance.

## Getting Started

### Prerequisites
Make sure you have Python installed, then install the required dependencies:
```bash
pip install opencv-python ultralytics pyttsx3
```

### Usage
Run one of the following scripts depending on your use case:

**1. Image Processing Mode**
Processes a static image and speaks the decision.
```bash
python main.py
```

**2. Video Processing Mode**
Processes a pre-recorded video file.
```bash
python video_navigation.py
```

**3. Live Camera Mode**
Uses your webcam for live navigation assistance.
```bash
python live_navigation.py
```

## Project Structure
- `vision/`: Contains scripts for object detection and distance estimation.
- `Planning/`: Contains the logic for the decision engine and collision warnings.
- `navigation/`: Handles the voice assistant implementation.
- `Models/`: YOLOv8 model weights.
