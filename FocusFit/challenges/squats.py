import cv2
import mediapipe as mp
import numpy as np
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.camera import OptimizedCamera
from utils.pose_detection import calculate_angle, get_pose_landmarks, draw_pose_landmarks, process_frame

mp_pose = mp.solutions.pose

def squat_detector(target_reps=5):
    """Enhanced squat detector with improved error handling"""
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
            ret, frame = cap.read()
            if not ret:
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
                hip = get_pose_landmarks(landmarks, "hip")
                knee = get_pose_landmarks(landmarks, "knee")
                ankle = get_pose_landmarks(landmarks, "ankle")

                if hip and knee and ankle:
                    angle = calculate_angle(hip, knee, ankle)

                    if angle < 90:
                        stage = "down"
                    if angle > 160 and stage == "down":
                        stage = "up"
                        reps += 1
                        print(f"🏋️ Squats: {reps}")

            except Exception as e:
                print(f"Error in pose detection: {e}")
                pass

            # Draw landmarks with error handling
            draw_pose_landmarks(frame, results)

            cv2.putText(frame, f"Squats: {reps}", (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 100, 0), 3, cv2.LINE_AA)

            cv2.imshow('FocusFit - Squats', frame)

            if reps >= target_reps:
                print("✅ Squats Complete! 🔓 UNLOCK!")
                break

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    squat_detector()
