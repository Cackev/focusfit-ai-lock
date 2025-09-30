import tkinter as tk
import time

def start_lock_timer(duration=60):  # duration in seconds
    """Show a fullscreen lock window with a countdown using Tk's after()."""
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(bg="#0d1117")
    root.title("FocusFit Lock")

    tk.Label(root, text="🔒 FocusFit Lock Active", font=("Segoe UI", 24, "bold"), bg="#0d1117", fg="#FF5555").pack(pady=50)
    timer_label = tk.Label(root, text="00:00", font=("Segoe UI", 48), bg="#0d1117", fg="#58A6FF")
    timer_label.pack(pady=10)
    tk.Label(root, text="Complete the challenge to unlock your session.", font=("Segoe UI", 14), bg="#0d1117", fg="white").pack(pady=10)

    # Prevent closing
    root.protocol("WM_DELETE_WINDOW", lambda: None)

    remaining = {'sec': duration}

    def tick():
        secs_left = remaining['sec']
        mins, secs = divmod(secs_left, 60)
        timer_label.config(text=f"{mins:02d}:{secs:02d}")
        if secs_left <= 0:
            root.destroy()  # Unlock
            return
        remaining['sec'] -= 1
        root.after(1000, tick)

    tick()
    root.mainloop()


if __name__ == "__main__":
    start_lock_timer(5)  # 10 seconds
