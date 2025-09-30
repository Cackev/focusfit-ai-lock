from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import os
import threading
from typing import Optional, Literal
from multiprocessing import Process, set_start_method
import subprocess
import shutil

# Existing app logic imports
from challenges import pushups, squats, jumpingjacks
from lock import start_lock_timer
from src.core.data_manager import DataManager
from src.core.goals_manager import GoalsManager

# Ensure a safe start method for subprocess UI work (Tkinter/OpenCV)
try:
    set_start_method('fork')
except RuntimeError:
    pass

# Constants and file paths reused from the Tkinter app
MODE_FILE = "focusfit_mode.json"
TIMES_FILE = "focusfit_times.json"
DATA_FILE = "focusfit_data.json"
GOALS_FILE = "focusfit_goals.json"

# Managers
data_manager = DataManager(DATA_FILE)
goals_manager = GoalsManager(GOALS_FILE)

# FastAPI app
app = FastAPI(title="FocusFit API", version="1.0.0")

# CORS for local dev (React, etc.)
ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Models
class TimesPayload(BaseModel):
    times: list[str]

class ModePayload(BaseModel):
    mode: Literal["strict", "normal"]

class ChallengePayload(BaseModel):
    challenge: Literal["Push-ups", "Squats", "Jumping Jacks"]
    reps: int

class GoalsUpdatePayload(BaseModel):
    reps: int

class MintPayload(BaseModel):
    to_address: str
    amount: str  # string to preserve precision; binary parses units


# Utilities mirroring main.py simple persistence for mode/times

def _read_json_file(path: str, default):
    try:
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return default


def _write_json_file(path: str, value) -> bool:
    try:
        with open(path, "w") as f:
            json.dump(value, f)
        return True
    except Exception:
        return False


def _load_mode() -> str:
    obj = _read_json_file(MODE_FILE, {"mode": "strict"})
    return obj.get("mode", "strict")


def _save_mode(mode: str) -> bool:
    return _write_json_file(MODE_FILE, {"mode": mode})


def _load_times() -> list[str]:
    return _read_json_file(TIMES_FILE, []) or []


def _save_times(times: list[str]) -> bool:
    return _write_json_file(TIMES_FILE, times)


# Challenge runner in a separate process (safe for Tkinter/OpenCV)

def _run_challenge_sync(challenge: str, reps: int):
    try:
        start_lock_timer(5)
        if challenge == "Push-ups":
            pushups.pushup_detector(target_reps=reps)
        elif challenge == "Squats":
            squats.squat_detector(target_reps=reps)
        elif challenge == "Jumping Jacks":
            jumpingjacks.jumping_jack_detector(target_reps=reps)
        data_manager.add_history_entry(challenge, reps)
        goals_manager.update_progress(reps)
    except Exception as e:
        print(f"Challenge process error: {e}")


# Token helpers

def _minter_path() -> Optional[str]:
    bin_path = os.path.join(os.path.dirname(__file__), "rust-mint", "target", "release", "focusfit-minter")
    return bin_path if os.path.exists(bin_path) and os.access(bin_path, os.X_OK) else None


# Routes

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/mode")
def get_mode():
    return {"mode": _load_mode()}


@app.post("/mode")
def set_mode(payload: ModePayload):
    if not _save_mode(payload.mode):
        raise HTTPException(status_code=500, detail="Failed to save mode")
    return {"ok": True, "mode": payload.mode}


@app.get("/times")
def get_times():
    return {"times": _load_times()}


@app.post("/times")
def set_times(payload: TimesPayload):
    # simple validation: HH:MM 24h
    validated: list[str] = []
    for t in payload.times:
        try:
            t = t.strip()
            h, m = map(int, t.split(":"))
            if 0 <= h < 24 and 0 <= m < 60:
                validated.append(f"{h:02d}:{m:02d}")
        except Exception:
            continue
    if len(validated) != len(payload.times):
        raise HTTPException(status_code=400, detail="Invalid time format. Use HH:MM 24h.")
    if not _save_times(validated):
        raise HTTPException(status_code=500, detail="Failed to save times")
    return {"ok": True, "times": validated}


@app.get("/history")
def get_history():
    return {"history": data_manager.get_history()}


@app.get("/goals")
def get_goals():
    daily = goals_manager.get_daily_progress()
    weekly = goals_manager.get_weekly_progress()
    daily_pct, weekly_pct = goals_manager.get_progress_percentage()
    return {
        "daily_reps": daily,
        "weekly_challenges": weekly,
        "daily_percent": daily_pct,
        "weekly_percent": weekly_pct,
        "daily_goal": goals_manager.DAILY_GOAL_REPS,
        "weekly_goal": goals_manager.WEEKLY_GOAL_CHALLENGES,
        "daily_goal_achieved": goals_manager.is_daily_goal_achieved(),
        "weekly_goal_achieved": goals_manager.is_weekly_goal_achieved(),
    }


@app.post("/goals/update")
def update_goals(payload: GoalsUpdatePayload):
    if payload.reps <= 0:
        raise HTTPException(status_code=400, detail="reps must be positive")
    ok = goals_manager.update_progress(payload.reps)
    if not ok:
        raise HTTPException(status_code=500, detail="Failed to update goals")
    return {"ok": True}


@app.post("/challenge/start")
def start_challenge(payload: ChallengePayload):
    if payload.reps <= 0:
        raise HTTPException(status_code=400, detail="reps must be positive")
    proc = Process(target=_run_challenge_sync, args=(payload.challenge, payload.reps))
    proc.start()
    return {"ok": True, "message": "Challenge started"}


@app.get("/token/check")
def token_check():
    bin_path = _minter_path()
    env = {k: os.environ.get(k) for k in ["RPC_URL", "PRIVATE_KEY", "TOKEN_ADDRESS", "TOKEN_DECIMALS"]}
    return {
        "binary": {"exists": bin_path is not None, "path": bin_path},
        "env": {k: bool(v) for k, v in env.items()},
    }


@app.post("/token/mint")
def token_mint(payload: MintPayload):
    bin_path = _minter_path()
    if not bin_path:
        raise HTTPException(status_code=400, detail="Minter binary not found. Build via cargo build --release in rust-mint/")
    if not payload.to_address or not payload.amount:
        raise HTTPException(status_code=400, detail="to_address and amount are required")
    try:
        rust_mint_dir = os.path.join(os.path.dirname(__file__), "rust-mint")
        env = os.environ.copy()  # allow server env to pass through
        result = subprocess.run(
            [bin_path, payload.to_address, payload.amount],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=rust_mint_dir,
            env=env,
        )
        ok = result.returncode == 0
        return {
            "ok": ok,
            "code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Minting timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Minting failed: {e}")


# Serve built frontend if available
DIST_DIR = os.path.join(os.path.dirname(__file__), "frontend", "dist")
INDEX_FILE = os.path.join(DIST_DIR, "index.html")
ASSETS_DIR = os.path.join(DIST_DIR, "assets")

if os.path.exists(DIST_DIR) and os.path.isfile(INDEX_FILE):
    if os.path.isdir(ASSETS_DIR):
        app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

    @app.get("/")
    def index():
        return FileResponse(INDEX_FILE)


# Convenience: uvicorn entrypoint
if __name__ == "__main__":
    import uvicorn
    # Disable reload to avoid killing active challenges when data files change
    uvicorn.run(
        "api_server:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
    )
