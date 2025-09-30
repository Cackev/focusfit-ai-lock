import cv2
import mediapipe as mp
import numpy as np
from typing import List, Optional, Tuple

# Pose modules
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(a: List[float], b: List[float], c: List[float]) -> float:
    """Calculate the angle between three points with improved accuracy"""
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return 360 - angle if angle > 180.0 else angle

def get_landmarks_safe(landmarks, pose_landmark) -> Optional[List[float]]:
    """Get landmarks with fallback to left side if right side is not visible"""
    try:
        # Try right side first
        right_landmark = landmarks[pose_landmark.value]
        if right_landmark.visibility > 0.5:
            return [right_landmark.x, right_landmark.y]
        
        # Fallback to left side
        left_landmark = landmarks[pose_landmark.value + 1]  # Left side landmarks
        if left_landmark.visibility > 0.5:
            return [left_landmark.x, left_landmark.y]
    except Exception:
        pass
    return None

def get_pose_landmarks(landmarks, landmark_type: str) -> Optional[List[float]]:
    """Get pose landmarks with proper error handling"""
    try:
        if landmark_type == "shoulder":
            return get_landmarks_safe(landmarks, mp_pose.PoseLandmark.RIGHT_SHOULDER)
        elif landmark_type == "elbow":
            return get_landmarks_safe(landmarks, mp_pose.PoseLandmark.RIGHT_ELBOW)
        elif landmark_type == "wrist":
            return get_landmarks_safe(landmarks, mp_pose.PoseLandmark.RIGHT_WRIST)
        elif landmark_type == "hip":
            return get_landmarks_safe(landmarks, mp_pose.PoseLandmark.RIGHT_HIP)
        elif landmark_type == "knee":
            return get_landmarks_safe(landmarks, mp_pose.PoseLandmark.RIGHT_KNEE)
        elif landmark_type == "ankle":
            return get_landmarks_safe(landmarks, mp_pose.PoseLandmark.RIGHT_ANKLE)
        elif landmark_type == "left_wrist":
            return [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        elif landmark_type == "right_wrist":
            return [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        elif landmark_type == "left_ankle":
            return [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
        elif landmark_type == "right_ankle":
            return [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
    except Exception:
        pass
    return None

def draw_pose_landmarks(frame, results):
    """Draw pose landmarks with error handling"""
    try:
        if results and results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    except Exception as e:
        print(f"Error drawing landmarks: {e}")

def process_frame(frame):
    """Process frame for pose detection with proper color conversion"""
    try:
        # Flip image for mirror effect
        frame = cv2.flip(frame, 1)
        # Convert color space
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame, rgb
    except Exception as e:
        print(f"Error processing frame: {e}")
        return frame, None

