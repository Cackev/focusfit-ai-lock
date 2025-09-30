import cv2
import mediapipe as mp
import numpy as np
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.camera import OptimizedCamera
from utils.pose_detection import get_pose_landmarks, draw_pose_landmarks, process_frame

mp_pose = mp.solutions.pose

def jumping_jack_detector(target_reps=5):
    """Enhanced jumping jack detector with improved error handling"""
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
                break

            # Process frame with improved utilities
            frame, rgb = process_frame(frame)
            if rgb is None:
                continue
                
            results = pose.process(rgb)
            frame = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark

                # Use improved landmark detection with fallback
                left_wrist = get_pose_landmarks(landmarks, "left_wrist")
                right_wrist = get_pose_landmarks(landmarks, "right_wrist")
                left_ankle = get_pose_landmarks(landmarks, "left_ankle")
                right_ankle = get_pose_landmarks(landmarks, "right_ankle")

                if left_wrist and right_wrist and left_ankle and right_ankle:
                    hands_up = left_wrist[1] < 0.3 and right_wrist[1] < 0.3
                    feet_apart = abs(left_ankle[0] - right_ankle[0]) > 0.5

                    if hands_up and feet_apart:
                        stage = "out"
                    if not hands_up and not feet_apart and stage == "out":
                        stage = "in"
                        reps += 1
                        print(f"🕺 Jumping Jacks: {reps}")

            except Exception as e:
                print(f"Error in pose detection: {e}")
                pass

            # Draw landmarks with error handling
            draw_pose_landmarks(frame, results)

            cv2.putText(frame, f'Jacks: {reps}', (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 150, 255), 3, cv2.LINE_AA)

            cv2.imshow("FocusFit - Jumping Jacks", frame)

            if reps >= target_reps:
                print("✅ Jumping Jacks Complete! 🔓 UNLOCK!")
                break

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    jumping_jack_detector()
