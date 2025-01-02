# Playback 👋 🎬

Playback is a Python-based gesture recognition system that allows you to control media playback using hand gestures captured through your webcam. It uses computer vision and hand tracking to provide a touchless media control experience.

## Features

- Real-time hand gesture detection
- Media playback control through hand movements
- Clean, modular, and type-safe Python implementation
- Configurable gesture thresholds and settings

## Supported Gestures

| Gesture | Action | Description |
|---------|--------|-------------|
| Pinch | Play/Pause | Bring thumb and index finger together |
| Left Hand | Rewind | Move hand to the left side of the frame |
| Right Hand | Forward | Move hand to the right side of the frame |

## Requirements

- Python 3.7+
- Webcam

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Shobhit-Nagpal/playback.git
cd playback
```

2. Install required packages:
```bash
pip install opencv-python mediapipe pyautogui numpy
```

## Usage

Run the main script:
```bash
python play.py
```

To exit the application, press 'q' while the window is in focus.

## Configuration

The application uses two configuration classes that can be customized:

### GestureConfig
```python
@dataclass
class GestureConfig:
    pinch_threshold: float = 0.1    # Sensitivity for pinch detection
    left_threshold: float = 0.3     # Left boundary for rewind gesture
    right_threshold: float = 0.7    # Right boundary for forward gesture
    cooldown: int = 10              # Frames to wait between gestures
```

### MediaConfig
```python
@dataclass
class MediaConfig:
    frame_width: int = 600         # Width of camera frame
    frame_height: int = 800        # Height of camera frame
    window_name: str = "HandFlix"  # Window title
```

## Project Structure

```
handflix/
│
├── play.py          # Main application file
├── README.md           # This file
```

## Code Structure

The project is organized into three main classes:

1. `GestureController`: Handles gesture recognition using MediaPipe
2. `MediaController`: Manages media control actions
3. `Playback`: Main application class that coordinates everything

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Common Issues

1. **Webcam not detected**: Ensure your webcam is properly connected and not being used by another application.
2. **MediaPipe installation**: If you encounter issues installing MediaPipe, try:
   ```bash
   pip install --upgrade pip
   pip install mediapipe
   ```
3. **Gesture sensitivity**: Adjust the thresholds in `GestureConfig` if gestures are too sensitive or not sensitive enough.

## Acknowledgments

- [MediaPipe](https://mediapipe.dev/) for hand tracking capabilities
- [OpenCV](https://opencv.org/) for computer vision functionality
- [PyAutoGUI](https://pyautogui.readthedocs.io/) for media control simulation
