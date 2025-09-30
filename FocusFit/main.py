import tkinter as tk
from tkinter import ttk, messagebox
from challenges import pushups, squats, jumpingjacks
from lock import start_lock_timer

import tkinter as tk
from tkinter import ttk, messagebox
from challenges import pushups, squats, jumpingjacks
from lock import start_lock_timer
import json, os
reminder_time = None
open_times = []

# --- Mode persistence ---
MODE_FILE = "focusfit_mode.json"
def load_mode():
    import json, os
    if os.path.exists(MODE_FILE):
        try:
            with open(MODE_FILE, "r") as f:
                return json.load(f).get("mode", "strict")
        except Exception:
            return "strict"
    return "strict"
def save_mode(mode):
    import json
    try:
        with open(MODE_FILE, "w") as f:
            json.dump({"mode": mode}, f)
    except Exception:
        pass

# Load allowed open times from file
TIMES_FILE = "focusfit_times.json"
def save_open_times():
    import json
    try:
        with open(TIMES_FILE, "w") as f:
            json.dump(open_times, f)
    except Exception:
        pass

def load_open_times():
    global open_times
    import json, os
    if os.path.exists(TIMES_FILE):
        try:
            with open(TIMES_FILE, "r") as f:
                open_times = json.load(f)
        except Exception:
            open_times = []
    else:
        open_times = []
load_open_times()

app_mode = load_mode()  # "strict" or "normal"

# Popup to set allowed open times
def show_times_popup():
    popup = tk.Toplevel(window)
    popup.title("Set Allowed Open Times")
    popup.geometry("340x260")
    popup.configure(bg="#161B22")
    tk.Label(popup, text="Add times when FocusFit can open (HH:MM, 24h):", font=("Segoe UI", 12), bg="#161B22", fg="#F0F6FC").pack(pady=12)
    times_var = tk.StringVar(value=", ".join(open_times))
    entry = tk.Entry(popup, textvariable=times_var, font=("Segoe UI", 12), justify='center', width=18)
    entry.pack(pady=8)
    def save_times():
        val = times_var.get().strip()
        times = [t.strip() for t in val.split(',') if t.strip()]
        # Validate times
        valid = True
        for t in times:
            try:
                h, m = map(int, t.split(':'))
                if not (0 <= h < 24 and 0 <= m < 60):
                    valid = False
            except Exception:
                valid = False
        if not valid:
            messagebox.showerror("Invalid Time", "Please enter times as HH:MM, separated by commas.")
            return
        global open_times
        open_times = times
        popup.destroy()
        save_open_times()
        messagebox.showinfo("Times Set", f"FocusFit will only open at: {', '.join(open_times)}")
    tk.Button(popup, text="Save Times", command=save_times, font=("Segoe UI", 12), bg="#238636", fg="white", relief="flat", padx=10, pady=6).pack(pady=14)

def show_reminder_popup():
    popup = tk.Toplevel(window)
    popup.title("Set Daily Reminder")
    popup.geometry("320x180")
    popup.configure(bg="#161B22")
    tk.Label(popup, text="Set a daily reminder time (24h):", font=("Segoe UI", 12), bg="#161B22", fg="#F0F6FC").pack(pady=16)
    time_var = tk.StringVar(value="18:00")
    entry = tk.Entry(popup, textvariable=time_var, font=("Segoe UI", 12), justify='center', width=8)
    entry.pack(pady=8)
    def set_reminder():
        global reminder_time
        val = time_var.get().strip()
        try:
            h, m = map(int, val.split(':'))
            if 0 <= h < 24 and 0 <= m < 60:
                reminder_time = f"{h:02d}:{m:02d}"
                popup.destroy()
                messagebox.showinfo("Reminder Set", f"Daily reminder set for {reminder_time}.")
            else:
                raise ValueError
        except Exception:
            messagebox.showerror("Invalid Time", "Please enter time as HH:MM (24h format).")
    tk.Button(popup, text="Set Reminder", command=set_reminder, font=("Segoe UI", 12), bg="#238636", fg="white", relief="flat", padx=10, pady=6).pack(pady=14)


# Check every minute for set times and auto-trigger challenge
def check_reminder():
    import datetime
    now = datetime.datetime.now().strftime('%H:%M')
    # If any open_time matches now, auto-trigger challenge
    if open_times:
        for t in open_times:
            if now == t:
                # Popup: Challenge time!
                challenge_popup = tk.Toplevel(window)
                challenge_popup.title("FocusFit Challenge Time!")
                challenge_popup.geometry("340x180")
                challenge_popup.configure(bg="#161B22")
                tk.Label(challenge_popup, text="It's time for your FocusFit Challenge!", font=("Segoe UI", 14, "bold"), bg="#161B22", fg="#3FB950").pack(pady=18)
                tk.Label(challenge_popup, text="Device will lock until challenge is complete.", font=("Segoe UI", 11), bg="#161B22", fg="#F0F6FC").pack(pady=4)
                def begin_auto_challenge():
                    challenge_popup.destroy()
                    # Start challenge and lock device
                    window.destroy()  # Close main window
                    start_lock_timer(5)
                    # Use default challenge (Push-ups, 5 reps) or last selected
                    try:
                        reps = int(reps_var.get())
                    except Exception:
                        reps = 5
                    challenge = challenge_var.get() if 'challenge_var' in globals() else "Push-ups"
                    if challenge == "Push-ups":
                        pushups.pushup_detector(target_reps=reps)
                    elif challenge == "Squats":
                        squats.squat_detector(target_reps=reps)
                    elif challenge == "Jumping Jacks":
                        jumpingjacks.jumping_jack_detector(target_reps=reps)
                    # After challenge, show success popup and re-open app
                    success_win = tk.Tk()
                    success_win.title("Success!")
                    success_win.geometry("320x120")
                    success_win.configure(bg="#161B22")
                    tk.Label(success_win, text="✅ Challenge Complete!", font=("Segoe UI", 18, "bold"), fg="#3FB950", bg="#161B22").pack(pady=20)
                    tk.Button(success_win, text="OK", command=success_win.destroy, font=("Segoe UI", 12), bg="#238636", fg="white", relief="flat").pack(pady=10)
                tk.Button(challenge_popup, text="Start Challenge", command=begin_auto_challenge, font=("Segoe UI", 12), bg="#238636", fg="white", relief="flat", padx=10, pady=6).pack(pady=18)
    # Only call after window is defined

# === Persistence Setup ===
DATA_FILE = "focusfit_data.json"
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
            return data.get("history", []), data.get("custom_challenges", [])
        except Exception:
            return [], []
    return [], []
def save_data():
    try:
        with open(DATA_FILE, "w") as f:
            json.dump({"history": history, "custom_challenges": custom_challenges}, f)
    except Exception:
        pass

# Load history and custom challenges
history, custom_challenges = load_data()

# === GUI Setup ===


# --- Only allow opening at set times if in strict mode ---
import datetime
def is_open_time():
    now = datetime.datetime.now()
    now_str = now.strftime('%H:%M')
    # Allow within ±5 minutes of any set time
    for t in open_times:
        try:
            h, m = map(int, t.split(':'))
            allowed = datetime.datetime(now.year, now.month, now.day, h, m)
            delta = abs((now - allowed).total_seconds())
            if delta <= 300:  # 5 minutes
                return True
        except Exception:
            continue
    return False if open_times else True  # If no times set, allow

if app_mode == "strict" and not is_open_time():
    temp = tk.Tk()
    temp.withdraw()
    messagebox.showwarning("FocusFit Locked", "FocusFit is only available at your set times!\nSet times using the 'Set Times' button or switch to Normal Mode in Settings.")
    temp.destroy()
    import sys
    sys.exit()

window = tk.Tk()
window.title("FocusFit Lock")
window.geometry("660x440")  # Wider for sidebar
window.minsize(560, 350)
window.configure(bg="#0D1117")
window.rowconfigure(1, weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=0)
window.after(60000, check_reminder)

# --- Goals Sidebar ---
goals_frame = tk.Frame(window, bg="#161B22", bd=0, relief="flat", highlightthickness=0)
goals_frame.grid(row=1, column=1, sticky="ns", padx=(0,10), pady=28)
goals_frame.grid_rowconfigure(0, weight=1)

# Daily/Weekly goals setup
DAILY_GOAL_REPS = 50
WEEKLY_GOAL_CHALLENGES = 5
def get_today():
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d')
def get_week():
    from datetime import datetime
    now = datetime.now()
    return f"{now.year}-W{now.isocalendar()[1]}"

# Load or initialize progress
import json, os
if os.path.exists("focusfit_goals.json"):
    try:
        with open("focusfit_goals.json", "r") as f:
            goals_data = json.load(f)
    except Exception:
        goals_data = {}
else:
    goals_data = {}
today = get_today()
week = get_week()
daily_reps = goals_data.get(today, {}).get("reps", 0)
weekly_challenges = goals_data.get(week, {}).get("challenges", 0)

def save_goals():
    goals_data[today] = {"reps": daily_reps}
    goals_data[week] = {"challenges": weekly_challenges}
    try:
        with open("focusfit_goals.json", "w") as f:
            json.dump(goals_data, f)
    except Exception:
        pass

def update_goals(reps):
    global daily_reps, weekly_challenges
    daily_reps += reps
    weekly_challenges += 1
    save_goals()
    update_goals_ui()

def update_goals_ui():
    daily_var.set(f"{min(daily_reps, DAILY_GOAL_REPS)}/{DAILY_GOAL_REPS} reps")
    weekly_var.set(f"{min(weekly_challenges, WEEKLY_GOAL_CHALLENGES)}/{WEEKLY_GOAL_CHALLENGES} challenges")
    daily_bar['value'] = min(daily_reps, DAILY_GOAL_REPS)
    weekly_bar['value'] = min(weekly_challenges, WEEKLY_GOAL_CHALLENGES)
    if daily_reps >= DAILY_GOAL_REPS:
        daily_status.config(text="Goal Achieved!", fg="#3FB950")
    else:
        daily_status.config(text="", fg="#F0F6FC")
    if weekly_challenges >= WEEKLY_GOAL_CHALLENGES:
        weekly_status.config(text="Goal Achieved!", fg="#3FB950")
    else:
        weekly_status.config(text="", fg="#F0F6FC")

tk.Label(goals_frame, text="🏆 Your Goals", font=("Segoe UI", 16, "bold"), bg="#161B22", fg="#F0F6FC").pack(pady=(0,18))
tk.Label(goals_frame, text="Daily Reps", font=("Segoe UI", 12), bg="#161B22", fg="#F0F6FC").pack(anchor="w", padx=8)
daily_var = tk.StringVar()
daily_bar = ttk.Progressbar(goals_frame, length=120, maximum=DAILY_GOAL_REPS)
daily_bar.pack(padx=8, pady=2)
tk.Label(goals_frame, textvariable=daily_var, font=("Segoe UI", 11), bg="#161B22", fg="#F0F6FC").pack(anchor="w", padx=8)
daily_status = tk.Label(goals_frame, text="", font=("Segoe UI", 11, "bold"), bg="#161B22", fg="#F0F6FC")
daily_status.pack(anchor="w", padx=8, pady=(0,10))
tk.Label(goals_frame, text="Weekly Challenges", font=("Segoe UI", 12), bg="#161B22", fg="#F0F6FC").pack(anchor="w", padx=8)
weekly_var = tk.StringVar()
weekly_bar = ttk.Progressbar(goals_frame, length=120, maximum=WEEKLY_GOAL_CHALLENGES)
weekly_bar.pack(padx=8, pady=2)
tk.Label(goals_frame, textvariable=weekly_var, font=("Segoe UI", 11), bg="#161B22", fg="#F0F6FC").pack(anchor="w", padx=8)
weekly_status = tk.Label(goals_frame, text="", font=("Segoe UI", 11, "bold"), bg="#161B22", fg="#F0F6FC")
weekly_status.pack(anchor="w", padx=8, pady=(0,10))
update_goals_ui()

def start_challenge():
    challenge = challenge_var.get()
    try:
        reps = int(reps_var.get())
        if reps <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Reps must be a positive number.")
        return

    # Animated countdown popup before starting challenge, with progress bar
    # Adapt colors to theme
    light_mode = window.cget("bg") == "#F0F6FC"
    popup_bg = "#E3E8EF" if light_mode else "#161B22"
    popup_fg = "#161B22" if light_mode else "#F0F6FC"
    accent_fg = "#238636" if light_mode else "#58A6FF"

    countdown_win = tk.Toplevel(window)
    countdown_win.title("Get Ready!")
    countdown_win.geometry("320x200")
    countdown_win.configure(bg=popup_bg)
    label = tk.Label(countdown_win, text="Challenge starts in...", font=("Segoe UI", 16, "bold"), fg=accent_fg, bg=popup_bg)
    label.pack(pady=20)
    timer_label = tk.Label(countdown_win, text="5", font=("Segoe UI", 44, "bold"), fg=popup_fg, bg=popup_bg)
    timer_label.pack(pady=10)
    progress = ttk.Progressbar(countdown_win, length=220, mode="determinate", maximum=5)
    progress.pack(pady=8)

    def add_to_history(challenge, reps):
        from datetime import datetime
        history.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {challenge} | {reps} reps")
        if len(history) > 10:
            history.pop(0)
        save_data()
        update_goals(reps)

    def countdown(t):
        if t > 0:
            timer_label.config(text=str(t))
            progress['value'] = 5 - t
            countdown_win.after(1000, lambda: countdown(t-1))
        else:
            progress['value'] = 5
            countdown_win.destroy()
            window.destroy()  # Close main window when challenge starts
            start_lock_timer(5)
            # Run challenge logic
            if challenge == "Push-ups":
                pushups.pushup_detector(target_reps=reps)
            elif challenge == "Squats":
                squats.squat_detector(target_reps=reps)
            elif challenge == "Jumping Jacks":
                jumpingjacks.jumping_jack_detector(target_reps=reps)
            # Add to history
            add_to_history(challenge, reps)
            # Show success popup after challenge
            success_win = tk.Tk()
            success_win.title("Success!")
            success_win.geometry("320x120")
            success_win.configure(bg="#161B22")
            tk.Label(success_win, text="✅ Challenge Complete!", font=("Segoe UI", 18, "bold"), fg="#3FB950", bg="#161B22").pack(pady=20)
            tk.Button(success_win, text="OK", command=success_win.destroy, font=("Segoe UI", 12), bg="#238636", fg="white", relief="flat").pack(pady=10)

    countdown(5)


# Theme switcher
def toggle_theme():
    current_bg = window.cget("bg")
    if current_bg == "#0D1117":
        window.configure(bg="#F0F6FC")
        header_frame.configure(bg="#F0F6FC")
        icon_label.configure(bg="#F0F6FC", fg="#238636")
        title_label.configure(bg="#F0F6FC", fg="#161B22")
        card_frame.configure(bg="#E3E8EF")
        for i, card in enumerate(card_widgets):
            if challenge_var.get() == challenge_names[i][0]:
                card.config(bg="#238636", fg="white", highlightbackground="#3FB950")
            else:
                card.config(bg="#E3E8EF", fg="#161B22", highlightbackground="#E3E8EF")
    else:
        window.configure(bg="#0D1117")
        header_frame.configure(bg="#0D1117")
        icon_label.configure(bg="#0D1117", fg="#58A6FF")
        title_label.configure(bg="#0D1117", fg="#F0F6FC")
        card_frame.configure(bg="#21262D")
        for i, card in enumerate(card_widgets):
            if challenge_var.get() == challenge_names[i][0]:
                card.config(bg="#238636", fg="white", highlightbackground="#3FB950")
            else:
                card.config(bg="#161B22", fg="#F0F6FC", highlightbackground="#21262D")

# Header icon and theme button
header_frame = tk.Frame(window, bg="#0D1117")
header_frame.grid(row=0, column=0, sticky="ew")
header_frame.grid_columnconfigure(0, weight=1)
icon_label = tk.Label(header_frame, text="🏋️‍♂️", font=("Segoe UI", 40), bg="#0D1117", fg="#58A6FF")
icon_label.pack(side="left", padx=(10, 18))
title_label = tk.Label(header_frame, text="FocusFit Challenge", font=("Segoe UI", 26, "bold"), bg="#0D1117", fg="#F0F6FC")
title_label.pack(side="left", padx=(0, 10))
theme_btn = tk.Button(header_frame, text="Toggle Theme", command=toggle_theme, font=("Segoe UI", 11, "bold"), bg="#444", fg="white", relief="flat", padx=12, pady=6)
theme_btn.pack(side="right", padx=18)

# Styling
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#0D1117", foreground="#F0F6FC", font=("Segoe UI", 12))
style.configure("TButton", background="#238636", foreground="white", font=("Segoe UI", 12, "bold"), padding=10, relief="flat")
style.map("TButton", background=[('active', '#2EA043')])
style.configure("TCombobox", fieldbackground="#161B22", background="#21262D", foreground="#F0F6FC", borderwidth=2)

# Card-style challenge selection
card_frame = tk.Frame(window, bg="#21262D", bd=0, relief="flat", highlightthickness=0)
card_frame.grid(row=1, column=0, sticky="nsew", padx=38, pady=28)
for i in range(4):
    card_frame.grid_columnconfigure(i, weight=1)
for r in range(5):
    card_frame.grid_rowconfigure(r, weight=1)

# Footer text and buttons
footer_frame = tk.Frame(window, bg="#0D1117")
footer_frame.grid(row=2, column=0, sticky="ew", pady=14)
window.geometry("500x440")
window.minsize(400, 350)
window.configure(bg="#0D1117")
window.rowconfigure(1, weight=1)
window.columnconfigure(0, weight=1)

# Theme switcher
def toggle_theme():
    current_bg = window.cget("bg")
    if current_bg == "#0D1117":
        window.configure(bg="#F0F6FC")
        header_frame.configure(bg="#F0F6FC")
        icon_label.configure(bg="#F0F6FC", fg="#238636")
        title_label.configure(bg="#F0F6FC", fg="#161B22")
        card_frame.configure(bg="#E3E8EF")
        for i, card in enumerate(card_widgets):
            if challenge_var.get() == challenge_names[i][0]:
                card.config(bg="#238636", fg="white", highlightbackground="#3FB950")
            else:
                card.config(bg="#E3E8EF", fg="#161B22", highlightbackground="#E3E8EF")
    else:
        window.configure(bg="#0D1117")
        header_frame.configure(bg="#0D1117")
        icon_label.configure(bg="#0D1117", fg="#58A6FF")
        title_label.configure(bg="#0D1117", fg="#F0F6FC")
        card_frame.configure(bg="#21262D")
        for i, card in enumerate(card_widgets):
            if challenge_var.get() == challenge_names[i][0]:
                card.config(bg="#238636", fg="white", highlightbackground="#3FB950")
            else:
                card.config(bg="#161B22", fg="#F0F6FC", highlightbackground="#21262D")

# Header icon and theme button
header_frame = tk.Frame(window, bg="#0D1117")
header_frame.grid(row=0, column=0, sticky="ew", pady=(18, 0))
header_frame.grid_columnconfigure(0, weight=1)
icon_label = tk.Label(header_frame, text="🏋️‍♂️", font=("Segoe UI", 40), bg="#0D1117", fg="#58A6FF")
icon_label.grid(row=0, column=0, padx=(10, 18), sticky="w")
title_label = tk.Label(header_frame, text="FocusFit Challenge", font=("Segoe UI", 26, "bold"), bg="#0D1117", fg="#F0F6FC")
title_label.grid(row=0, column=1, padx=(0, 10), sticky="w")
theme_btn = tk.Button(header_frame, text="Toggle Theme", command=toggle_theme, font=("Segoe UI", 11, "bold"), bg="#444", fg="white", relief="flat", padx=12, pady=6)
theme_btn.grid(row=0, column=2, padx=18, sticky="e")

# Styling
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#0D1117", foreground="#F0F6FC", font=("Segoe UI", 12))
style.configure("TButton", background="#238636", foreground="white", font=("Segoe UI", 12, "bold"), padding=10, relief="flat")
style.map("TButton", background=[('active', '#2EA043')])
style.configure("TCombobox", fieldbackground="#161B22", background="#21262D", foreground="#F0F6FC", borderwidth=2)

# === GUI Layout ===

# Card-style layout for challenge selection

# --- Card-style challenge selection ---
card_frame = tk.Frame(window, bg="#21262D", bd=0, relief="flat", highlightthickness=0)
card_frame.grid(row=1, column=0, sticky="nsew", padx=38, pady=28)
for i in range(4):
    card_frame.grid_columnconfigure(i, weight=1)
for r in range(5):
    card_frame.grid_rowconfigure(r, weight=1)

# --- Custom challenge creation ---
def open_create_challenge():
    popup = tk.Toplevel(window)
    popup.title("Create Challenge")
    popup.geometry("320x260")
    popup.configure(bg="#161B22")
    tk.Label(popup, text="Challenge Name:", font=("Segoe UI", 12), fg="#F0F6FC", bg="#161B22").pack(pady=(18,4))
    name_var = tk.StringVar()
    tk.Entry(popup, textvariable=name_var, font=("Segoe UI", 12), bg="#21262D", fg="#F0F6FC").pack(pady=4)
    tk.Label(popup, text="Target Reps:", font=("Segoe UI", 12), fg="#F0F6FC", bg="#161B22").pack(pady=(10,4))
    reps_var_popup = tk.StringVar()
    tk.Entry(popup, textvariable=reps_var_popup, font=("Segoe UI", 12), bg="#21262D", fg="#F0F6FC").pack(pady=4)
    tk.Label(popup, text="Icon (emoji):", font=("Segoe UI", 12), fg="#F0F6FC", bg="#161B22").pack(pady=(10,4))
    icon_var = tk.StringVar()
    tk.Entry(popup, textvariable=icon_var, font=("Segoe UI", 12), bg="#21262D", fg="#F0F6FC").pack(pady=4)
    def add_challenge():
        name = name_var.get().strip()
        reps = reps_var_popup.get().strip()
        icon = icon_var.get().strip() or "🏋️"
        if not name or not reps.isdigit() or int(reps) <= 0:
            messagebox.showerror("Invalid Input", "Please enter a valid name and positive number of reps.")
            return
        challenge_names.append((name, icon))
        custom_challenges.append([name, icon])
        save_data()
        # Add new card
        idx = len(challenge_names) - 1
        card = tk.Label(card_frame, text=f"{icon}  {name}", font=("Segoe UI", 16, "bold"), bg="#161B22", fg="#F0F6FC", bd=2, relief="ridge", padx=18, pady=16, cursor="hand2", highlightbackground="#21262D", highlightthickness=1)
        card.grid(row=1, column=idx, padx=14, pady=(0,14), sticky="nsew")
        card.bind("<Button-1>", lambda e, idx=idx: select_card(idx))
        def on_enter(e, idx=idx):
            if challenge_var.get() != challenge_names[idx][0]:
                card.config(bg="#2EA043", fg="white", highlightbackground="#3FB950")
        def on_leave(e, idx=idx):
            if challenge_var.get() != challenge_names[idx][0]:
                card.config(bg="#161B22", fg="#F0F6FC", highlightbackground="#21262D")
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        card_widgets.append(card)
        card_frame.grid_columnconfigure(idx, weight=1)
        select_card(idx)
        popup.destroy()
    tk.Button(popup, text="Add Challenge", command=add_challenge, font=("Segoe UI", 12, "bold"), bg="#238636", fg="white", relief="flat", padx=10, pady=6).pack(pady=18)

create_btn = tk.Button(card_frame, text="➕ Create Challenge", command=open_create_challenge, font=("Segoe UI", 12, "bold"), bg="#444", fg="white", relief="flat", padx=10, pady=6)
create_btn.grid(row=0, column=3, padx=(18,0), pady=(10,2), sticky="ew")
create_btn.bind("<Enter>", lambda e: create_btn.config(bg="#238636"))
create_btn.bind("<Leave>", lambda e: create_btn.config(bg="#444"))

tk.Label(card_frame, text="Choose a Challenge:", font=("Segoe UI", 12), bg="#21262D", fg="#F0F6FC").grid(row=0, column=0, columnspan=3, pady=(10,2), sticky="ew")

challenge_var = tk.StringVar(value="Push-ups")

# Built-in challenges
challenge_names = [
    ("Push-ups", "🏋️"),
    ("Squats", "🦵"),
    ("Jumping Jacks", "🤸")
]
# Add custom challenges loaded from file
for c in custom_challenges:
    if isinstance(c, list) and len(c) == 2:
        challenge_names.append(tuple(c))

card_widgets = []
def select_card(idx):
    challenge_var.set(challenge_names[idx][0])
    for i, card in enumerate(card_widgets):
        if i == idx:
            card.config(bg="#238636", fg="white", highlightbackground="#3FB950", highlightthickness=2, bd=2)
        else:
            card.config(bg="#161B22", fg="#F0F6FC", highlightbackground="#21262D", highlightthickness=1, bd=2)

for i, (name, icon) in enumerate(challenge_names):
    card = tk.Label(card_frame, text=f"{icon}  {name}", font=("Segoe UI", 16, "bold"), bg="#161B22", fg="#F0F6FC", bd=2, relief="ridge", padx=18, pady=16, cursor="hand2", highlightbackground="#21262D", highlightthickness=1)
    card.grid(row=1, column=i, padx=14, pady=(0,14), sticky="nsew")
    card.bind("<Button-1>", lambda e, idx=i: select_card(idx))
    def on_enter(e, idx=i):
        if challenge_var.get() != challenge_names[idx][0]:
            card.config(bg="#2EA043", fg="white", highlightbackground="#3FB950")
    def on_leave(e, idx=i):
        if challenge_var.get() != challenge_names[idx][0]:
            card.config(bg="#161B22", fg="#F0F6FC", highlightbackground="#21262D")
    card.bind("<Enter>", on_enter)
    card.bind("<Leave>", on_leave)
    card_widgets.append(card)
select_card(0)

tk.Label(card_frame, text="Target Reps:", font=("Segoe UI", 12), bg="#21262D", fg="#F0F6FC").grid(row=2, column=0, columnspan=3, pady=(0,2), sticky="ew")
reps_var = tk.StringVar(value="5")
tk.Entry(card_frame, textvariable=reps_var, font=("Segoe UI", 12), justify='center', relief="flat", bd=2, bg="#161B22", fg="#F0F6FC").grid(row=3, column=0, columnspan=3, pady=(0,10), ipadx=4, ipady=4, sticky="nsew")

start_btn = ttk.Button(card_frame, text="🚀 Start Challenge", command=start_challenge)
start_btn = ttk.Button(card_frame, text="🚀 Start Challenge", command=start_challenge)
start_btn.grid(row=4, column=0, columnspan=3, pady=22, sticky="nsew")
start_btn.configure(style="TButton")

# Footer text and buttons
footer_frame = tk.Frame(window, bg="#0D1117")
footer_frame.grid(row=2, column=0, sticky="ew", pady=14)
footer_frame.grid_columnconfigure(0, weight=1)

# Motivational quotes rotation
quotes = [
    "Discipline is choosing between what you want now and what you want most.",
    "Success is the sum of small efforts repeated day in and day out.",
    "Push yourself, because no one else is going to do it for you.",
    "The only bad workout is the one that didn’t happen.",
    "Don’t limit your challenges. Challenge your limits."
]
quote_var = tk.StringVar(value=quotes[0])
def rotate_quote():
    current = quotes.index(quote_var.get()) if quote_var.get() in quotes else 0
    next_idx = (current + 1) % len(quotes)
    quote_var.set(quotes[next_idx])
    window.after(6000, rotate_quote)
window.after(6000, rotate_quote)

quote_label = tk.Label(footer_frame, textvariable=quote_var, font=("Segoe UI", 11, "italic"), fg="#8B949E", bg="#0D1117", wraplength=420, justify="center")
quote_label.grid(row=0, column=0, pady=6, sticky="ew")
footer_text = tk.Label(footer_frame, text="💪 Stay fit. Stay focused. Get rewarded.", font=("Segoe UI", 10, "bold"), fg="#3FB950", bg="#0D1117")
footer_text.grid(row=1, column=0, pady=(0,4), sticky="ew")

# About/Settings/Leaderboard buttons
btn_frame = tk.Frame(footer_frame, bg="#0D1117")
btn_frame.grid(row=2, column=0, pady=6, sticky="ew")
def on_btn_enter(e):
    e.widget.config(bg="#238636")
def on_btn_leave(e):
    e.widget.config(bg="#444")
def show_leaderboard():
    lb_win = tk.Toplevel(window)
    lb_win.title("Leaderboard & History")
    lb_win.geometry("380x320")
    lb_win.configure(bg="#161B22")
    tk.Label(lb_win, text="Recent Challenges", font=("Segoe UI", 15, "bold"), fg="#3FB950", bg="#161B22").pack(pady=12)
    frame = tk.Frame(lb_win, bg="#161B22")
    frame.pack(fill="both", expand=True, padx=16, pady=8)
    if 'history' in globals() and history:
        for entry in reversed(history):
            tk.Label(frame, text=entry, font=("Segoe UI", 11), fg="#F0F6FC", bg="#161B22", anchor="w", justify="left").pack(fill="x", pady=2)
    else:
        tk.Label(frame, text="No challenges yet.", font=("Segoe UI", 11), fg="#8B949E", bg="#161B22").pack(pady=20)
    tk.Button(lb_win, text="Close", command=lb_win.destroy, font=("Segoe UI", 11), bg="#238636", fg="white", relief="flat", padx=10, pady=4).pack(pady=10)

# --- Achievements/Badges ---
def show_achievements():
    ach_win = tk.Toplevel(window)
    ach_win.title("Achievements & Badges")
    ach_win.geometry("420x340")
    ach_win.configure(bg="#161B22")
    tk.Label(ach_win, text="🏅 Achievements", font=("Segoe UI", 16, "bold"), bg="#161B22", fg="#F0F6FC").pack(pady=12)

    # Calculate achievements
    total_reps = sum(int(entry.split('|')[2].strip().split()[0]) for entry in history if '|' in entry)
    total_challenges = len(history)
    badges = []
    # Reps milestones
    if total_reps >= 100:
        badges.append(("100 Reps", "💯"))
    if total_reps >= 500:
        badges.append(("500 Reps", "🏆"))
    if total_reps >= 1000:
        badges.append(("1000 Reps", "🥇"))
    # Challenge milestones
    if total_challenges >= 10:
        badges.append(("10 Challenges", "🎉"))
    if total_challenges >= 50:
        badges.append(("50 Challenges", "🏅"))
    if total_challenges >= 100:
        badges.append(("100 Challenges", "🥈"))
    # Custom challenge badge
    if any(c for c in custom_challenges):
        badges.append(("Custom Creator", "🛠️"))

    # Display badges
    badge_frame = tk.Frame(ach_win, bg="#161B22")
    badge_frame.pack(pady=8)
    if badges:
        for name, icon in badges:
            tk.Label(badge_frame, text=f"{icon}  {name}", font=("Segoe UI", 14, "bold"), bg="#161B22", fg="#3FB950").pack(anchor="w", pady=4, padx=18)
    else:
        tk.Label(badge_frame, text="No badges unlocked yet.", font=("Segoe UI", 12), bg="#161B22", fg="#8B949E").pack(pady=18)

    # Progress toward next badge
    next_rep = next((x for x in [100,500,1000] if total_reps < x), None)
    next_chal = next((x for x in [10,50,100] if total_challenges < x), None)
    progress_frame = tk.Frame(ach_win, bg="#161B22")
    progress_frame.pack(pady=8)
    if next_rep:
        tk.Label(progress_frame, text=f"Reps to next badge: {next_rep-total_reps}", font=("Segoe UI", 12), bg="#161B22", fg="#F0F6FC").pack(anchor="w", padx=18)
    if next_chal:
        tk.Label(progress_frame, text=f"Challenges to next badge: {next_chal-total_challenges}", font=("Segoe UI", 12), bg="#161B22", fg="#F0F6FC").pack(anchor="w", padx=18)

    tk.Button(ach_win, text="Close", command=ach_win.destroy, font=("Segoe UI", 11), bg="#238636", fg="white", relief="flat", padx=10, pady=4).pack(pady=10)

# --- Statistics Dashboard ---
def show_stats():
    import datetime
    stats_win = tk.Toplevel(window)
    stats_win.title("Your Stats")
    stats_win.geometry("420x340")
    stats_win.configure(bg="#161B22")
    tk.Label(stats_win, text="📊 Statistics Dashboard", font=("Segoe UI", 16, "bold"), bg="#161B22", fg="#F0F6FC").pack(pady=12)

    # Parse history for stats
    total_reps = 0
    total_challenges = 0
    today_reps = 0
    week_reps = 0
    today_challenges = 0
    week_challenges = 0
    daily_counts = {}
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    week = datetime.datetime.now().isocalendar()[1]
    for entry in history:
        try:
            date_str, _, reps_str = entry.split('|')
            date = date_str.strip().split(' ')[0]
            reps = int(reps_str.strip().split()[0])
            total_reps += reps
            total_challenges += 1
            # Daily count
            daily_counts[date] = daily_counts.get(date, 0) + reps
            # Today
            if date == today:
                today_reps += reps
                today_challenges += 1
            # This week
            entry_week = datetime.datetime.strptime(date, '%Y-%m-%d').isocalendar()[1]
            if entry_week == week:
                week_reps += reps
                week_challenges += 1
        except Exception:
            continue

    # Stats summary
    stats_frame = tk.Frame(stats_win, bg="#161B22")
    stats_frame.pack(pady=6)
    tk.Label(stats_frame, text=f"Total Reps: {total_reps}", font=("Segoe UI", 12), bg="#161B22", fg="#F0F6FC").pack(anchor="w")
    tk.Label(stats_frame, text=f"Total Challenges: {total_challenges}", font=("Segoe UI", 12), bg="#161B22", fg="#F0F6FC").pack(anchor="w")
    tk.Label(stats_frame, text=f"Reps Today: {today_reps}", font=("Segoe UI", 12), bg="#161B22", fg="#3FB950").pack(anchor="w")
    tk.Label(stats_frame, text=f"Challenges Today: {today_challenges}", font=("Segoe UI", 12), bg="#161B22", fg="#3FB950").pack(anchor="w")
    tk.Label(stats_frame, text=f"Reps This Week: {week_reps}", font=("Segoe UI", 12), bg="#161B22", fg="#58A6FF").pack(anchor="w")
    tk.Label(stats_frame, text=f"Challenges This Week: {week_challenges}", font=("Segoe UI", 12), bg="#161B22", fg="#58A6FF").pack(anchor="w")

    # Bar chart for last 7 days
    chart_frame = tk.Frame(stats_win, bg="#161B22")
    chart_frame.pack(pady=10)
    tk.Label(chart_frame, text="Daily Reps (Last 7 Days)", font=("Segoe UI", 12, "bold"), bg="#161B22", fg="#F0F6FC").pack()
    from datetime import datetime, timedelta
    days = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6,-1,-1)]
    max_reps = max([daily_counts.get(day,0) for day in days]+[1])
    for day in days:
        reps = daily_counts.get(day,0)
        bar_len = int(180 * reps / max_reps) if max_reps else 0
        bar_color = "#3FB950" if reps > 0 else "#444"
        day_label = datetime.strptime(day, '%Y-%m-%d').strftime('%a')
        row = tk.Frame(chart_frame, bg="#161B22")
        row.pack(fill="x", padx=8, pady=2)
        tk.Label(row, text=day_label, width=4, font=("Segoe UI", 11), bg="#161B22", fg="#8B949E").pack(side="left")
        tk.Label(row, text=f"{reps:3d}", width=4, font=("Segoe UI", 11), bg="#161B22", fg="#F0F6FC").pack(side="left")
        bar = tk.Frame(row, bg=bar_color, height=16, width=bar_len)
        bar.pack(side="left", padx=4)

    tk.Button(stats_win, text="Close", command=stats_win.destroy, font=("Segoe UI", 11), bg="#238636", fg="white", relief="flat", padx=10, pady=4).pack(pady=10)

leaderboard_btn = tk.Button(btn_frame, text="Leaderboard", font=("Segoe UI", 10, "bold"), bg="#444", fg="white", relief="flat", padx=10, pady=4, command=show_leaderboard)
leaderboard_btn.pack(side="left", padx=8)
leaderboard_btn.bind("<Enter>", on_btn_enter)
leaderboard_btn.bind("<Leave>", on_btn_leave)
stats_btn = tk.Button(btn_frame, text="Stats", font=("Segoe UI", 10, "bold"), bg="#444", fg="white", relief="flat", padx=10, pady=4, command=show_stats)
stats_btn.pack(side="left", padx=8)
stats_btn.bind("<Enter>", on_btn_enter)
stats_btn.bind("<Leave>", on_btn_leave)
ach_btn = tk.Button(btn_frame, text="Achievements", font=("Segoe UI", 10, "bold"), bg="#444", fg="white", relief="flat", padx=10, pady=4, command=show_achievements)
ach_btn.pack(side="left", padx=8)
ach_btn.bind("<Enter>", on_btn_enter)
ach_btn.bind("<Leave>", on_btn_leave)

reminder_btn = tk.Button(btn_frame, text="Set Reminder", font=("Segoe UI", 10, "bold"), bg="#444", fg="white", relief="flat", padx=10, pady=4, command=show_reminder_popup)
reminder_btn.pack(side="left", padx=8)
reminder_btn.bind("<Enter>", on_btn_enter)
reminder_btn.bind("<Leave>", on_btn_leave)

# New: Set Times button
times_btn = tk.Button(btn_frame, text="Set Times", font=("Segoe UI", 10, "bold"), bg="#444", fg="white", relief="flat", padx=10, pady=4, command=show_times_popup)
times_btn.pack(side="left", padx=8)
times_btn.bind("<Enter>", on_btn_enter)
times_btn.bind("<Leave>", on_btn_leave)

about_btn = tk.Button(btn_frame, text="About", font=("Segoe UI", 10, "bold"), bg="#444", fg="white", relief="flat", padx=10, pady=4, command=lambda: messagebox.showinfo("About", "FocusFit v1.0\nCreated by your team."))
about_btn.pack(side="left", padx=8)
about_btn.bind("<Enter>", on_btn_enter)
about_btn.bind("<Leave>", on_btn_leave)

# --- Settings popup with mode toggle ---
def show_settings():
    popup = tk.Toplevel(window)
    popup.title("Settings")
    popup.geometry("340x220")
    popup.configure(bg="#161B22")
    tk.Label(popup, text="App Mode:", font=("Segoe UI", 13, "bold"), bg="#161B22", fg="#F0F6FC").pack(pady=(18,8))
    mode_var = tk.StringVar(value=app_mode)
    def set_mode():
        global app_mode
        app_mode = mode_var.get()
        save_mode(app_mode)
        popup.destroy()
        messagebox.showinfo("Mode Changed", f"App mode set to: {'Strict' if app_mode=='strict' else 'Normal'}")
    strict_radio = tk.Radiobutton(popup, text="Strict Mode (locked, only open at set times)", variable=mode_var, value="strict", font=("Segoe UI", 11), bg="#161B22", fg="#F0F6FC", selectcolor="#161B22", anchor="w")
    strict_radio.pack(fill="x", padx=18, pady=2)
    normal_radio = tk.Radiobutton(popup, text="Normal Mode (open anytime)", variable=mode_var, value="normal", font=("Segoe UI", 11), bg="#161B22", fg="#F0F6FC", selectcolor="#161B22", anchor="w")
    normal_radio.pack(fill="x", padx=18, pady=2)
    tk.Button(popup, text="Save", command=set_mode, font=("Segoe UI", 12), bg="#238636", fg="white", relief="flat", padx=10, pady=6).pack(pady=18)

settings_btn = tk.Button(btn_frame, text="Settings", font=("Segoe UI", 10, "bold"), bg="#444", fg="white", relief="flat", padx=10, pady=4, command=show_settings)
settings_btn.pack(side="left", padx=8)
settings_btn.bind("<Enter>", on_btn_enter)
settings_btn.bind("<Leave>", on_btn_leave)

window.mainloop()
