import cv2
import mediapipe as mp
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
# Set up audio control with pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_range = volume.GetVolumeRange()
min_vol = vol_range[0]
max_vol = vol_range[1]
with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]  
                thumb_x, thumb_y = int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0])
                index_x, index_y = int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0])
                cv2.circle(frame, (thumb_x, thumb_y), 10, (255, 0, 0), cv2.FILLED)
                cv2.circle(frame, (index_x, index_y), 10, (255, 0, 0), cv2.FILLED)
                cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), (0, 255, 0), 3)
                length = np.hypot(index_x - thumb_x, index_y - thumb_y)
                vol = np.interp(length, [20, 200], [min_vol, max_vol])
                volume.SetMasterVolumeLevel(vol, None)
                cv2.putText(frame, f'Volume: {int(np.interp(vol, [min_vol, max_vol], [0, 100]))}%', 
                            (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

        cv2.imshow('Hand Tracking - Volume Control', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
