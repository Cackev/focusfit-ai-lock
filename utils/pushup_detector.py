# utils/pushup_detector.py
import cv2
import mediapipe as mp

class PushupDetector:
    def __init__(self, target_reps=10):
        self.target_reps = target_reps
        self.reps = 0
        self.direction = 0  # 0: going down, 1: going up
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_draw = mp.solutions.drawing_utils

    def calculate_angle(self, a, b, c):
        import numpy as np
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle
        return angle

    def detect(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            success, img = cap.read()
            if not success:
                break
            
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.pose.process(img_rgb)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                shoulder = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                         landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                         landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                angle = self.calculate_angle(shoulder, elbow, wrist)

                if angle < 90:
                    if self.direction == 0:
                        self.reps += 0.5
                        self.direction = 1
                if angle > 160:
                    if self.direction == 1:
                        self.reps += 0.5
                        self.direction = 0

                if self.reps >= self.target_reps:
                    break

                self.mp_draw.draw_landmarks(img, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
                cv2.putText(img, f'Reps: {int(self.reps)}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            cv2.imshow('Pushup Challenge', img)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
