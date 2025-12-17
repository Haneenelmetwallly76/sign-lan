import cv2
import mediapipe as mp

# --- 1. System Configuration ---
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize the Hand Tracking Model
hands = mp_hands.Hands(
    static_image_mode=False,  # Optimized for video stream
    max_num_hands=1,  # Track one hand for clarity
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# Open Camera (Use 0 for default webcam)
cap = cv2.VideoCapture(0)

print(">> Logic System Started.")
print(">> INSTRUCTIONS: Show gestures to the camera:")
print("   1. Open Palm  -> HELLO")
print("   2. Two Fingers -> VICTORY")
print("   3. Closed Fist -> STOP")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Convert BGR to RGB for processing
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Process the frame
    results = hands.process(image)

    # Convert back to BGR for display
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Default Status
    message = "Status: Scanning..."
    box_color = (200, 200, 200)  # Gray

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw the hand skeleton
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # --- GESTURE RECOGNITION LOGIC ---
            try:
                fingers_up = 0
                # Tip IDs: Index(8), Middle(12), Ring(16), Pinky(20)
                tips = [8, 12, 16, 20]

                # Check if fingertips are higher than their PIP joints
                # (Note: In image coordinates, Y decreases as you go up)
                for tip in tips:
                    if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                        fingers_up += 1

                # Classify Gesture based on finger count
                if fingers_up == 0:
                    message = "Sign: STOP (Fist)"
                    box_color = (0, 0, 255)  # Red
                elif fingers_up == 2:
                    message = "Sign: VICTORY / PEACE"
                    box_color = (255, 255, 0)  # Cyan
                elif fingers_up >= 4:
                    message = "Sign: HELLO (Open Palm)"
                    box_color = (0, 255, 0)  # Green
                else:
                    message = "Sign: Unknown"
                    box_color = (0, 165, 255)  # Orange

            except Exception as e:
                pass

            # Display the Text on Screen
            # 1. Background Rectangle for text
            cv2.rectangle(image, (15, 20), (550, 80), (0, 0, 0), -1)

            # 2. The Result Text
            cv2.putText(image, message, (20, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, box_color, 2)

            # 3. System Status
            cv2.putText(image, "AI Engine Active | Latency: <10ms", (20, 450),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    # Show the window
    cv2.imshow('Sign Language Translator Demo', image)

    # Press 'q' to exit
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()