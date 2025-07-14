# challenges/squats.py

import cv2
import mediapipe as mp

def run(target_reps=20):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    count = 0
    position = None

    print(f"[INFO] Start doing squats. Target: {target_reps}")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(rgb)

        if result.pose_landmarks:
            mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            left_hip = result.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y
            left_knee = result.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].y

            ratio = left_hip / left_knee

            if ratio < 0.85:
                if position != "down":
                    position = "down"
            elif ratio > 0.95:
                if position == "down":
                    position = "up"
                    count += 1
                    print(f"Squat count: {count}")

        cv2.putText(frame, f"Squats: {count}/{target_reps}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 0), 2)

        cv2.imshow("Squat Tracker", frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

        if count >= target_reps:
            print("[SUCCESS] Target reached!")
            break

    cap.release()
    cv2.destroyAllWindows()
