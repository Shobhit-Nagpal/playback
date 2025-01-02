import cv2
import time
import mediapipe as mp

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, value=600)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, value=800)

mp_hands = mp.solutions.hands
hand = mp_hands.Hands()

while True:
    success, frame = cap.read()
    if success:
        RGB_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hand.process(RGB_frame)
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                print(hand_landmarks)

        cv2.imshow(winname="capture image", mat=frame)
        if cv2.waitKey(1) == ord("q"):
            break

cv2.destroyAllWindows()