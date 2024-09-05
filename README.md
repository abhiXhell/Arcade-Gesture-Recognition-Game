# Gesture Recognition Arcade Game 🎮✋

This is a gesture recognition-based arcade game where players replicate hand gestures displayed on the screen. A robotic arm rewards the player with toffees based on their performance. The game uses Mediapipe for hand gesture detection and Pygame for the game window and sounds.

## Features
- Detects multiple hand gestures using Mediapipe.
- Displays random gestures for the player to replicate.
- Countdown before capturing gestures.
- Sound effects for cheering, clapping, and game over.
- Integration with robotic arm to dispense toffees based on performance.

## Technologies Used
- **OpenCV** for capturing video and image processing.
- **Mediapipe** for hand gesture detection.
- **Pygame** for game rendering and sound management.

## Getting Started

### Prerequisites
- Python 3.x
- Virtual environment (optional but recommended)

### Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/abhiXhell/GestureRecognitionArcadeGame.git
    cd Arcade-Gesture-Recognition-Game
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the game:
    ```bash
    python main.py
    ```

## Controls
- **Camera**: The game automatically detects your gestures using your webcam.
- **Gestures**: Replicate the gestures shown on the screen to score points.
