# main.py

import tkinter as tk
from tkinter import messagebox
from challenges import pushups, squats, jumpingjacks

def start_challenge():
    choice = selected_challenge.get()
    try:
        reps = int(reps_entry.get())
        if reps <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number of reps.")
        return

    window.destroy()

    if choice == "Push-Ups":
        pushups.run(reps)
    elif choice == "Squats":
        squats.run(reps)
    elif choice == "Jumping Jacks":
        jumpingjacks.run(reps)

# Initialize UI
window = tk.Tk()
window.title("AI Fitness Lock - Select Challenge")
window.geometry("350x300")
window.resizable(False, False)

# Dropdown menu
tk.Label(window, text="Choose Challenge:", font=("Arial", 14)).pack(pady=10)
selected_challenge = tk.StringVar(value="Push-Ups")
options = ["Push-Ups", "Squats", "Jumping Jacks"]
tk.OptionMenu(window, selected_challenge, *options).pack()

# Reps input
tk.Label(window, text="Number of Reps:", font=("Arial", 12)).pack(pady=10)
reps_entry = tk.Entry(window, font=("Arial", 12))
reps_entry.insert(0, "20")
reps_entry.pack()

# Start button
tk.Button(window, text="Start Challenge", font=("Arial", 13), command=start_challenge).pack(pady=20)

window.mainloop()
