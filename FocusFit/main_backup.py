import tkinter as tk
from tkinter import ttk, messagebox
from challenges import pushups, squats, jumpingjacks
from lock import start_lock_timer

def start_challenge():
    challenge = challenge_var.get()
    try:
        reps = int(reps_var.get())
        if reps <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Reps must be a positive number.")
        return

    window.destroy()

    start_lock_timer(5)

    if challenge == "Push-ups":
        pushups.pushup_detector(target_reps=reps)
    elif challenge == "Squats":
        squats.squat_detector(target_reps=reps)
    elif challenge == "Jumping Jacks":
        jumpingjacks.jumping_jack_detector(target_reps=reps)

# === GUI Setup ===
window = tk.Tk()
window.title("🏋️‍♂️ FocusFit Lock")
window.geometry("480x400")
window.configure(bg="#0D1117")

# Styling
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#0D1117", foreground="#F0F6FC", font=("Segoe UI", 12))
style.configure("TButton", background="#238636", foreground="white", font=("Segoe UI", 11), padding=8)
style.map("TButton", background=[('active', '#2EA043')])
style.configure("TCombobox", fieldbackground="#161B22", background="#21262D", foreground="#F0F6FC")

# === GUI Layout ===
tk.Label(window, text="🎯 FocusFit Challenge", bg="#0D1117", fg="#58A6FF", font=("Segoe UI", 18, "bold")).pack(pady=20)

# Challenge dropdown
tk.Label(window, text="Choose a Challenge:", font=("Segoe UI", 11)).pack(pady=5)
challenge_var = tk.StringVar(value="Push-ups")
ttk.Combobox(window, textvariable=challenge_var, values=["Push-ups", "Squats", "Jumping Jacks"], font=("Segoe UI", 11)).pack()

# Reps input
tk.Label(window, text="Target Reps:", font=("Segoe UI", 11)).pack(pady=10)
reps_var = tk.StringVar(value="5")
tk.Entry(window, textvariable=reps_var, font=("Segoe UI", 11), justify='center').pack(ipady=4)

# Start button
ttk.Button(window, text="🚀 Start Challenge", command=start_challenge).pack(pady=25)

# Footer text
tk.Label(window, text="“Discipline is choosing between what you want now\nand what you want most.”", font=("Segoe UI", 10, "italic"), fg="#8B949E", bg="#0D1117").pack(pady=10)

tk.Label(window, text="💪 Stay fit. Stay focused. Get rewarded.", font=("Segoe UI", 9), fg="#3FB950", bg="#0D1117").pack()

window.mainloop()
