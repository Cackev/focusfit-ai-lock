# 🔐 FocusFit – AI Fitness Lock

> Unlock your device using physical fitness challenges like push-ups, squats, or jumping jacks.

## 🎯 What is FocusFit?

**FocusFit** is an AI-powered desktop lock system that verifies physical activity (e.g., 20 push-ups) using computer vision. Only after completing the challenge, your system unlocks. It’s perfect for enforcing health, productivity, and self-discipline.

## 🧠 Key Features
- Camera-based detection using **MediaPipe + OpenCV**
- Supports **push-ups**, **squats**, and **jumping jacks**
- Adjustable target reps
- Built-in lock timer
- Rewards tracked using **Rust smart contracts** on **Avalanche Blockchain**

## 🔧 Tech Stack
- Python (MediaPipe, OpenCV, PyQt5)
- Rust (ethers-rs, Avalanche C-Chain)
- GitHub + VS Code
- Future: Electron / Flutter GUI

## 🖼 Demo
![Push-Up Detection](assets/demo-pushup.gif) <!-- Replace with actual image or gif -->

## 🚀 How to Run

```bash
git clone https://github.com/KevinKyuli/focusfit-ai-lock.git
cd focusfit-ai-lock
python main.py
