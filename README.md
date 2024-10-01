# Gesture Controlled Volume Control

This project demonstrates a gesture-based system for controlling the volume of your computer using hand gestures detected through a webcam. It uses Python's `OpenCV` library for real-time video capture, `MediaPipe` for hand detection, and a system control package like `pycaw` to control the system's audio volume.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How it Works](#how-it-works)
- [License](#license)

## Overview
In this project, a user can raise or lower the system's volume using simple hand gestures. The project detects the hand landmarks using MediaPipe and calculates the distance between the thumb and index finger. This distance is then mapped to control the volume of the system in real-time.

## Features
- **Real-Time Hand Tracking**: Detects hand gestures in real-time using the webcam feed.
- **Volume Control**: Adjusts the system's audio volume based on hand gestures.
- **Efficient**: Uses MediaPipe for fast and accurate hand landmark detection.
- **User-Friendly**: Intuitive hand gestures for volume control.

## Requirements
To run the project, you'll need the following:

- Python 3.x
- `OpenCV` for video capture and image processing
- `MediaPipe` for hand gesture detection
- `pycaw` for controlling the system's audio volume on Windows
- `numpy` for numerical operations

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/gesture-controlled-volume.git
    cd gesture-controlled-volume
    ```

2. Install the required dependencies:
    ```bash
    pip install opencv-python mediapipe numpy pycaw
    ```

## Usage

1. Run the script:
    ```bash
    python gesture_controlled_volume.py
    ```

2. The webcam will open and start detecting your hand. Move your thumb and index finger to adjust the volume.
   - **Increase volume**: Spread your thumb and index finger apart.
   - **Decrease volume**: Bring your thumb and index finger closer together.

3. To exit the program, press `q` or close the webcam window.

## How it Works

- **MediaPipe Hand Detection**: The system uses MediaPipe to detect 21 landmarks on the hand, focusing on the thumb and index finger. 
- **Distance Calculation**: The distance between the tip of the thumb and the tip of the index finger is calculated using Euclidean distance.
- **Volume Control**: The distance is mapped to the system volume using `pycaw`. The farther apart your fingers are, the higher the volume will be, and vice versa.

### Main Libraries
- `OpenCV`: Handles video stream and image processing.
- `MediaPipe`: Provides efficient and accurate hand tracking.
- `pycaw`: Controls the system audio on Windows.

### Code Snippet (Gesture to Volume Mapping)
```python
# Calculate distance between thumb and index finger tips
thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

# Get pixel positions of the tips
thumb_x, thumb_y = int(thumb_tip.x * width), int(thumb_tip.y * height)
index_x, index_y = int(index_tip.x * width), int(index_tip.y * height)

# Calculate the distance
distance = np.hypot(index_x - thumb_x, index_y - thumb_y)

# Map the distance to the system's volume range (0 to 100)
volume = np.interp(distance, [min_distance, max_distance], [0, 100])

# Set the volume using pycaw
volume_control.SetMasterVolumeLevelScalar(volume / 100, None)
```


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
