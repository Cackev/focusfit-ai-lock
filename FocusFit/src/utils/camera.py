import cv2
import time
from typing import Optional

class OptimizedCamera:
    """Enhanced camera handling with better error handling and performance optimization"""
    
    def __init__(self, target_fps=30):
        self.target_fps = target_fps
        self.frame_time = 1.0 / target_fps
        self.last_frame_time = 0
        self.cap = None
    
    def get_camera(self) -> cv2.VideoCapture:
        """Get camera with improved error handling and multiple fallback options"""
        # Try multiple camera indices
        for i in range(3):  # Try /dev/video0, /dev/video1, /dev/video2
            try:
                cap = cv2.VideoCapture(i, cv2.CAP_V4L2)
                if cap.isOpened():
                    print(f"✅ Camera found at index {i}")
                    self.cap = cap
                    return cap
            except Exception as e:
                print(f"Camera {i} failed: {e}")
        
        # Fallback to default camera
        try:
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                print("✅ Using fallback camera")
                self.cap = cap
                return cap
        except Exception as e:
            print(f"Fallback camera failed: {e}")
        
        raise RuntimeError("No working camera found")
    
    def get_frame(self):
        """Get frame with frame rate limiting for better performance"""
        if not self.cap:
            return None, None
        
        current_time = time.time()
        if current_time - self.last_frame_time < self.frame_time:
            return None, None
        
        self.last_frame_time = current_time
        return self.cap.read()
    
    def release(self):
        """Properly release camera resources"""
        if self.cap:
            self.cap.release()
            self.cap = None

