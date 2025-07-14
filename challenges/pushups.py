# challenges/pushups.py

import cv2
import mediapipe as mp

def run(target_reps=20):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)

    count = 0
    position = None

    print(f"[INFO] Start doing push-ups. Target: {target_reps}")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(rgb)

        if result.pose_landmarks:
            mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            left_shoulder = result.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y
            left_hip = result.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y

            ratio = left_shoulder / left_hip

            # Heuristic thresholds (adjust as needed)
            if ratio < 0.9:
                if position != "down":
                    position = "down"
            elif ratio > 1.05:
                if position == "down":
                    position = "up"
                    count += 1
                    print(f"Push-up count: {count}")

        cv2.putText(frame, f"Push-ups: {count}/{target_reps}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Push-up Tracker", frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

        if count >= target_reps:
            print("[SUCCESS] Target reached!")
            break

    cap.release()
    cv2.destroyAllWindows()
