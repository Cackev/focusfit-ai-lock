# challenges/jumpingjacks.py

from utils.jumpingjack_detector import detect_jumpingjacks

def run_jumpingjacks_challenge(target_reps=10):
    print("Starting Jumping Jacks Challenge...")
    result = detect_jumpingjacks(target_reps=target_reps)
    print("Challenge Complete!")
    print(f"Reps: {result['reps']} | Duration: {result['duration_sec']} seconds")
