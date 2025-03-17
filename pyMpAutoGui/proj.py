import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)

screen_width, screen_height = pyautogui.size()
prev_x, prev_y = 0, 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            landmarks = hand_landmarks.landmark
            index_finger = landmarks[8]
            thumb_tip = landmarks[4]
            middle_finger = landmarks[12]
            ring_finger = landmarks[16]
            pinky_finger = landmarks[20]
            
            x, y = int(index_finger.x * screen_width), int(index_finger.y * screen_height)
            
            # Draw keypoints on frame
            for i, landmark in enumerate(landmarks):
                h, w, _ = frame.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(frame, (cx, cy), 5, (255, 0, 255), -1)
                cv2.putText(frame, str(i), (cx + 5, cy - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Move mouse cursor
            smooth_x = prev_x + (x - prev_x) * 0.2
            smooth_y = prev_y + (y - prev_y) * 0.2
            pyautogui.moveTo(smooth_x, smooth_y)
            prev_x, prev_y = smooth_x, smooth_y
            
            # Click gesture (thumb and index touching)
            if abs(index_finger.x - thumb_tip.x) < 0.03 and abs(index_finger.y - thumb_tip.y) < 0.03:
                pyautogui.click()
                cv2.putText(frame, "Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Scroll Up/Down (Middle and Index finger vertical difference)
            if abs(index_finger.y - middle_finger.y) > 0.05:
                if index_finger.y > middle_finger.y:
                    pyautogui.scroll(-10)
                else:
                    pyautogui.scroll(10)
                cv2.putText(frame, "Scrolling", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
            # Close Window (Fist Gesture: all fingers close together)
            if (
                abs(index_finger.x - pinky_finger.x) < 0.05
                and abs(index_finger.y - pinky_finger.y) < 0.05
                and abs(thumb_tip.y - pinky_finger.y) < 0.05
            ):
                pyautogui.hotkey('alt', 'f4')
                cv2.putText(frame, "Closing Window", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.namedWindow("Hand Control", cv2.WINDOW_NORMAL)
    cv2.imshow("Hand Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
