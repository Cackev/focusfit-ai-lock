# FocusFit - Fitness-Focused Productivity App

A Python application that combines computer vision, blockchain rewards, and time management to help users stay fit and focused.

## 🚀 Features

- **Computer Vision Challenges**: Push-ups, squats, and jumping jacks detection
- **Time Management**: Strict mode with scheduled unlock times
- **Progress Tracking**: Daily and weekly goals with statistics
- **Blockchain Integration**: Rust-based token minting system
- **Custom Challenges**: Create your own fitness challenges
- **Achievement System**: Badges and progress tracking

## 📋 Requirements

```bash
pip install -r requirements.txt
```

### Dependencies
- `opencv-python>=4.8.0` - Computer vision
- `mediapipe>=0.10.0` - Pose detection
- `numpy>=1.24.0` - Numerical computations
- `Pillow>=9.0.0` - Image processing

## 🏗️ Project Structure

```
FocusFit/
├── src/                          # Improved source code
│   ├── utils/
│   │   ├── camera.py            # Enhanced camera handling
│   │   └── pose_detection.py    # Improved pose detection
│   └── core/
│       ├── data_manager.py      # Data management with backups
│       └── goals_manager.py     # Goals tracking
├── challenges/                   # Exercise detection modules
│   ├── pushups.py
│   ├── squats.py
│   └── jumpingjacks.py
├── rust-mint/                   # Blockchain integration
├── main.py                      # Main application
├── lock.py                      # Screen lock functionality
└── requirements.txt             # Python dependencies
```

## 🔧 Improvements Made

### 1. **Enhanced Error Handling**
- Better camera detection with multiple fallback options
- Graceful handling of pose detection failures
- Improved data validation and backup systems

### 2. **Performance Optimizations**
- Frame rate limiting for better CPU usage
- Optimized camera resource management
- Improved memory usage patterns

### 3. **Code Organization**
- Modular structure with separate utilities
- Better separation of concerns
- Improved maintainability

### 4. **Data Management**
- Automatic backup creation
- Data validation and error recovery
- Export functionality

### 5. **Pose Detection Enhancements**
- Fallback to left side landmarks if right side fails
- Better angle calculation accuracy
- Improved landmark detection reliability

## 🎯 Usage

### Basic Usage
```bash
python main.py
```

### Testing Individual Challenges
```bash
python challenges/pushups.py
python challenges/squats.py
python challenges/jumpingjacks.py
```

### Blockchain Integration
```bash
cd rust-mint
cargo build --release
./target/release/focusfit-minter <wallet_address> <amount>
```

## ⚙️ Configuration

### App Modes
- **Strict Mode**: Only opens at scheduled times
- **Normal Mode**: Opens anytime

### Settings
- Set allowed open times
- Configure daily reminders
- Customize challenge parameters

## 📊 Features

### Progress Tracking
- Daily rep goals (50 reps)
- Weekly challenge goals (5 challenges)
- Achievement badges
- Statistics dashboard

### Custom Challenges
- Create custom exercises
- Set target reps
- Choose custom icons

### Time Management
- Scheduled unlock times
- Daily reminders
- Focus mode with device locking

## 🔒 Privacy & Security

- Local data storage
- No cloud dependencies
- Camera permissions handled gracefully
- Data backup and export options

## 🐛 Troubleshooting

### Camera Issues
- Try different camera indices (0, 1, 2)
- Check camera permissions
- Verify OpenCV installation

### Pose Detection Issues
- Ensure good lighting
- Stand at appropriate distance
- Check MediaPipe installation

### Data Issues
- Check file permissions
- Verify JSON file integrity
- Use backup files if needed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- MediaPipe for pose detection
- OpenCV for computer vision
- Ethers.rs for blockchain integration
- Tkinter for GUI framework

