# rock-paper-scissors
rock-paper-scissors using mediapipe
Sure, here's a README file for your GitHub repository explaining your Python code:

---

# Rock Paper Scissors Hand Gesture Game

This Python script implements a simple hand gesture-based game of Rock Paper Scissors using the OpenCV and MediaPipe libraries. The game detects hand gestures using a webcam and allows two players to compete against each other.

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- MediaPipe (`mediapipe`)
- Protobuf library (`google.protobuf.json_format.MessageToDict`)

## Installation

1. Install Python if you haven't already: [Python Downloads](https://www.python.org/downloads/)
2. Install required libraries using pip:
    ```
    pip install opencv-python mediapipe protobuf
    ```

## Usage

1. Clone the repository or download the script file (`rock_paper_scissors.py`) to your local machine.
2. Run the script using Python:
    ```
    python rock_paper_scissors.py
    ```
3. Follow the on-screen instructions to play the game. The game requires a webcam to detect hand gestures.

## How it works

1. The script uses the webcam to capture frames.
2. It utilizes the MediaPipe library to detect hand landmarks in each frame.
3. Based on the position of the landmarks, it determines the hand gesture (rock, paper, or scissors).
4. Players are prompted to show their gestures, and the game evaluates the winner based on the rules of Rock Paper Scissors.
5. The game keeps track of scores and displays them on the screen.

## Notes

- Make sure to play the game in a well-lit environment for better hand detection.
- Only the signs for rock, paper, and scissors are allowed. Any other signs may result in improper detection.

---

You can use this README file to provide clear instructions and information about your project on GitHub. Feel free to customize it further based on your preferences or additional features of your project!
