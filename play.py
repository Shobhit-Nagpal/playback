from enum import Enum
from dataclasses import dataclass
import mediapipe as mp
import numpy as np
import cv2
from typing import Tuple, Optional
import pyautogui


# Gestures

class Gesture(Enum):
    REWIND = "REWIND"
    FORWARD = "FORWARD"
    TOGGLE_PLAY = "PLAY/PAUSE"
    NOP = "NOP"


@dataclass
class GestureConfig:
    pinch_threshold: float = 0.1
    left_threshold: float = 0.2
    right_threshold: float = 0.8
    cooldown: int = 7


class GestureController:
    def __init__(self, config: GestureConfig):
        self.config = config
        self.mp_hands = mp.solutions.hands
        self.hand = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.prev_gesture = Gesture.NOP
        self.cooldown = 0

    def _calculate_distance(self, p1, p2) -> float:
        return np.sqrt(
            (p1.x - p2.x) ** 2 +
            (p1.y - p2.y) ** 2
        )

    def _calculate_hand_position(self, landmarks) -> float:
        return np.mean([lm.x for lm in landmarks.landmark])

    def detect_gesture(self, hand_landmarks) -> Gesture:
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]

        distance = self._calculate_distance(thumb_tip, index_tip)

        hand_x = self._calculate_hand_position(hand_landmarks)

        if distance < self.config.pinch_threshold:
            return Gesture.TOGGLE_PLAY
        elif hand_x > self.config.left_threshold:
            return Gesture.REWIND
        elif hand_x < self.config.right_threshold:
            return Gesture.FORWARD

        return Gesture.NOP

    def process_frame(self, frame) -> Tuple[Optional[Gesture], np.ndarray]:
        if self.cooldown > 0:
            self.cooldown -= 1
            return None, frame

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hand.process(rgb_frame)

        detected_gesture = None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )
                current_gesture = self.detect_gesture(hand_landmarks)

                if current_gesture != self.prev_gesture:
                    detected_gesture = current_gesture
                    self.prev_gesture = current_gesture
                    self.cooldown = self.config.cooldown

        return detected_gesture, frame


class MediaAction(Enum):
    PLAY = "PLAY"
    PAUSE = "PAUSE"
    FORWARD = "FORWARD"
    REWIND = "REWIND"


@dataclass
class MediaConfig:
    frame_width: int = 800
    frame_height: int = 800
    window_name: str = "Playback"


class MediaController:
    def __init__(self):
        self.action_map = {
            Gesture.TOGGLE_PLAY: self._toggle_play,
            Gesture.REWIND: self._rewind,
            Gesture.FORWARD: self._forward
        }

    def _toggle_play(self):
        pyautogui.press("space")
        return "Play/Pause"

    def _rewind(self):
        pyautogui.press("left")
        return "Rewind"

    def _forward(self):
        pyautogui.press("right")
        return "Forward"

    def execute_action(self, gesture: Gesture) -> str:
        if gesture in self.action_map:
            return self.action_map[gesture]()

        return "No action"


class Playback:
    def __init__(self, gesture_config: GestureConfig, media_config: MediaConfig):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, value=600)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, value=600)

        self.gesture_ctl = GestureController(gesture_config)
        self.media_ctl = MediaController()
        self.win_name = media_config.window_name

    def run(self):
        try:
            while True:
                success, frame = self.cap.read()
                if not success:
                    break

                # Process frame and detect gesture
                gesture, processed_frame = self.gesture_ctl.process_frame(frame)

                # Execute media action if gesture detected
                if gesture:
                    action_text = self.media_ctl.execute_action(gesture)
                    # Display action text
                    cv2.putText(
                        processed_frame,
                        f"Action: {action_text}",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2
                    )

                # Display frame
                cv2.imshow(self.win_name, processed_frame)
                # Check for exit command
                if cv2.waitKey(1) == ord("q"):
                    break

        finally:
            self.cleanup()

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()


def main():
    # Initialize with default configurations
    gesture_config = GestureConfig()
    media_config = MediaConfig()
    # Create and run HandFlix
    app = Playback(gesture_config, media_config)
    app.run()


if __name__ == "__main__":
    main()
