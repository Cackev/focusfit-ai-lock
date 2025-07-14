# utils/jumpingjack_detector.py

import cv2
import mediapipe as mp
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    import numpy as np
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

def run_jumping_jack_detector(target_reps):
    cap = cv2.VideoCapture(0)

    counter = 0
    stage = None

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
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

                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

                angle = calculate_angle(left_wrist, left_shoulder, left_hip)

                if angle > 150:
                    stage = "up"
                if angle < 80 and stage == "up":
                    stage = "down"
                    counter += 1
                    print(f"Reps: {counter}")

            except:
                pass

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            cv2.putText(image, f'Reps: {counter}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            cv2.imshow('Jumping Jack Detection', image)

            if cv2.waitKey(10) & 0xFF == ord('q') or counter >= target_reps:
                break

    cap.release()
    cv2.destroyAllWindows()

    print(f"✅ Target of {target_reps} jumping jacks completed!")
# utils/jumpingjack_detector.py

import cv2
import mediapipe as mp
import time

mp_pose = mp.solutions.pose

def detect_jumpingjacks(target_reps=10):
    cap = cv2.VideoCapture(0)
    pose = mp_pose.Pose()
    reps = 0
    stage = None
    start_time = time.time()

    print("Do your jumping jacks in front of the camera!")

    while cap.isOpened() and reps < target_reps:
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        if results.pose_landmarks:
            left_hand = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
            right_hand = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
            left_foot = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]
            right_foot = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]

            hands_up = left_hand.y < 0.4 and right_hand.y < 0.4
            feet_apart = abs(left_foot.x - right_foot.x) > 0.4

            if hands_up and feet_apart:
                if stage == "down":
                    reps += 1
                    print(f"Repetition: {reps}")
                    stage = "up"
            else:
                if stage == "up":
                    stage = "down"

        cv2.imshow('Jumping Jacks Detector', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return {
        "reps": reps,
        "duration_sec": round(time.time() - start_time, 2)
    }
