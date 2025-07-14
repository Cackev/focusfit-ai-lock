# utils/squat_detector.py

import cv2
import mediapipe as mp
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def detect_squats(target_reps=5):
    cap = cv2.VideoCapture(0)
    counter = 0
    stage = None
    squat_depth_threshold = 0.4  # adjustable depending on your camera angle

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        start_time = time.time()
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark
                hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
                knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
                ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]

                # Squat logic using vertical movement
                hip_y = hip.y
                knee_y = knee.y

                if hip_y > knee_y + squat_depth_threshold:
                    stage = "down"
                if stage == "down" and hip_y < knee_y + 0.1:
                    stage = "up"
                    counter += 1
                    print(f"Reps: {counter}")

            except:
                pass

            # Draw pose landmarks
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Display count
            cv2.putText(image, f'Squats: {counter}', (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)

            cv2.imshow('Squat Detector', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            if counter >= target_reps:
                break

        cap.release()
        cv2.destroyAllWindows()
        duration = int(time.time() - start_time)
        return {
            "exercise": "squats",
            "reps": counter,
            "duration_sec": duration,
        }
