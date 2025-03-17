import cv2
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set width
cap.set(4, 720)   # Set height

screen_width, screen_height = pyautogui.size()
prev_x, prev_y = 0, 0

# Define the original size for the control area (16:9 aspect ratio)
original_width = 300
original_height = int(original_width * 9 / 16)

# Increase control area size by 1.5 times
control_area_width = int(original_width * 1.5)
control_area_height = int(original_height * 1.5)

# Set control area to the lower right corner
control_area_x = 1280 - control_area_width - 20
control_area_y = 720 - control_area_height - 20

# Default cursor control keypoint (thumb)
cursor_control_keypoint = 4  # Thumb

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    h, w, _ = frame.shape
    center_x, center_y = control_area_x + control_area_width // 2, control_area_y + control_area_height // 2
    
    # Draw center square in the lower right corner with updated size
    cv2.rectangle(frame, (control_area_x, control_area_y),
                  (control_area_x + control_area_width, control_area_y + control_area_height), (0, 255, 0), 2)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            landmarks = hand_landmarks.landmark
            cursor_finger = landmarks[cursor_control_keypoint]  # Use thumb for cursor movement
            thumb_tip = landmarks[4]
            index_tip = landmarks[8]
            
            # Normalize coordinates to the new control area (lower-right corner)
            x = int(cursor_finger.x * w)
            y = int(cursor_finger.y * h)
            
            if (control_area_x <= x <= control_area_x + control_area_width and
                control_area_y <= y <= control_area_y + control_area_height):
                mapped_x = ((x - control_area_x) / control_area_width) * screen_width
                mapped_y = ((y - control_area_y) / control_area_height) * screen_height
                
                # Move mouse cursor
                smooth_x = prev_x + (mapped_x - prev_x) * 0.2
                smooth_y = prev_y + (mapped_y - prev_y) * 0.2
                pyautogui.moveTo(smooth_x, smooth_y)
                prev_x, prev_y = smooth_x, smooth_y
            
            # Draw keypoints on frame
            for i, landmark in enumerate(landmarks):
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(frame, (cx, cy), 5, (255, 0, 255), -1)
                cv2.putText(frame, str(i), (cx + 5, cy - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Click and hold gesture (thumb and index touching)
            if abs(index_tip.x - thumb_tip.x) < 0.03 and abs(index_tip.y - thumb_tip.y) < 0.03:
                pyautogui.mouseDown()  # Click and hold
                cv2.putText(frame, "Click & Hold", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                pyautogui.mouseUp()  # Release the click
            
    cv2.imshow("Hand Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
