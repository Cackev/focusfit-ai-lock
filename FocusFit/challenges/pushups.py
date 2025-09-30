import cv2
import mediapipe as mp
import numpy as np
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.camera import OptimizedCamera
from utils.pose_detection import calculate_angle, get_pose_landmarks, draw_pose_landmarks, process_frame

# Pose modules
mp_pose = mp.solutions.pose

def pushup_detector(target_reps=5):
    """Enhanced pushup detector with improved error handling"""
    camera = OptimizedCamera()
    
    try:
        cap = camera.get_camera()
    except RuntimeError as e:
        print(f"❌ Camera error: {e}")
        return
    
    reps = 0
    stage = None

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("❌ Camera frame not captured")
                break

            # Process frame with improved utilities
            frame, rgb = process_frame(frame)
            if rgb is None:
                continue
                
            results = pose.process(rgb)

            # Convert back
            frame = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark

                # Use improved landmark detection with fallback
                shoulder = get_pose_landmarks(landmarks, "shoulder")
                elbow = get_pose_landmarks(landmarks, "elbow")
                wrist = get_pose_landmarks(landmarks, "wrist")

                if shoulder and elbow and wrist:
                    angle = calculate_angle(shoulder, elbow, wrist)

                    # Push-up stage logic
                    if angle < 90:
                        stage = "down"
                    if angle > 160 and stage == "down":
                        stage = "up"
                        reps += 1
                        print(f"💪 Push-Up Count: {reps}")

            except Exception as e:
                print(f"Error in pose detection: {e}")
                pass

            # Draw landmarks with error handling
            draw_pose_landmarks(frame, results)

            # Show count on screen
            cv2.putText(frame, f"Reps: {reps}", (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3, cv2.LINE_AA)

            cv2.imshow("FocusFit Push-Up Challenge", frame)

            # Exit or complete
            if reps >= target_reps:
                print("✅ Challenge Complete! 🔓 UNLOCK!")
                break

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    camera.release()
    cv2.destroyAllWindows()

# Run this file directly to test
if __name__ == "__main__":
    pushup_detector(target_reps=5)

