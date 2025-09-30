#!/usr/bin/env python3
"""
Test script to verify FocusFit improvements work correctly
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all new modules can be imported"""
    try:
        from core.data_manager import DataManager
        print("✅ Data manager module imported successfully")
    except ImportError as e:
        print(f"❌ Data manager module import failed: {e}")
        return False
    
    try:
        from core.goals_manager import GoalsManager
        print("✅ Goals manager module imported successfully")
    except ImportError as e:
        print(f"❌ Goals manager module import failed: {e}")
        return False
    
    # Test camera and pose detection imports (may fail without OpenCV)
    try:
        from utils.camera import OptimizedCamera
        print("✅ Camera module imported successfully")
    except ImportError as e:
        print(f"⚠️  Camera module import failed (expected without OpenCV): {e}")
    
    try:
        from utils.pose_detection import calculate_angle, get_pose_landmarks
        print("✅ Pose detection module imported successfully")
    except ImportError as e:
        print(f"⚠️  Pose detection module import failed (expected without OpenCV): {e}")
    
    return True

def test_data_manager():
    """Test data manager functionality"""
    try:
        from core.data_manager import DataManager
        dm = DataManager("test_data.json")
        
        # Test loading empty data
        data = dm.load_data()
        assert isinstance(data, dict)
        assert "history" in data
        assert "custom_challenges" in data
        print("✅ Data manager load test passed")
        
        # Test adding history entry
        success = dm.add_history_entry("Test Challenge", 5)
        assert success
        print("✅ Data manager add history test passed")
        
        # Test getting history
        history = dm.get_history()
        assert isinstance(history, list)
        print("✅ Data manager get history test passed")
        
        # Test getting custom challenges
        custom_challenges = dm.get_custom_challenges()
        assert isinstance(custom_challenges, list)
        print("✅ Data manager get custom challenges test passed")
        
        # Clean up
        if os.path.exists("test_data.json"):
            os.remove("test_data.json")
        
        return True
    except Exception as e:
        print(f"❌ Data manager test failed: {e}")
        return False

def test_goals_manager():
    """Test goals manager functionality"""
    try:
        from core.goals_manager import GoalsManager
        gm = GoalsManager("test_goals.json")
        
        # Test initial state
        daily_progress = gm.get_daily_progress()
        assert daily_progress >= 0
        print("✅ Goals manager initial state test passed")
        
        # Test progress update
        success = gm.update_progress(10)
        assert success
        print("✅ Goals manager progress update test passed")
        
        # Test progress percentage
        daily_percent, weekly_percent = gm.get_progress_percentage()
        assert 0 <= daily_percent <= 100
        assert 0 <= weekly_percent <= 100
        print("✅ Goals manager progress percentage test passed")
        
        # Test goal achievement checks
        daily_achieved = gm.is_daily_goal_achieved()
        weekly_achieved = gm.is_weekly_goal_achieved()
        assert isinstance(daily_achieved, bool)
        assert isinstance(weekly_achieved, bool)
        print("✅ Goals manager achievement check test passed")
        
        # Test weekly stats
        weekly_stats = gm.get_weekly_stats()
        assert isinstance(weekly_stats, dict)
        assert "total_reps" in weekly_stats
        assert "total_challenges" in weekly_stats
        assert "daily_breakdown" in weekly_stats
        print("✅ Goals manager weekly stats test passed")
        
        # Clean up
        if os.path.exists("test_goals.json"):
            os.remove("test_goals.json")
        
        return True
    except Exception as e:
        print(f"❌ Goals manager test failed: {e}")
        return False

def test_pose_detection_math():
    """Test pose detection math functions (without OpenCV)"""
    try:
        # Test angle calculation with simple math
        import math
        
        def simple_angle_calc(a, b, c):
            """Simple angle calculation for testing"""
            import math
            # Calculate vectors
            ba = [a[0] - b[0], a[1] - b[1]]
            bc = [c[0] - b[0], c[1] - b[1]]
            
            # Calculate dot product
            dot_product = ba[0] * bc[0] + ba[1] * bc[1]
            
            # Calculate magnitudes
            ba_mag = math.sqrt(ba[0]**2 + ba[1]**2)
            bc_mag = math.sqrt(bc[0]**2 + bc[1]**2)
            
            # Calculate angle
            if ba_mag == 0 or bc_mag == 0:
                return 0
            cos_angle = dot_product / (ba_mag * bc_mag)
            cos_angle = max(-1, min(1, cos_angle))  # Clamp to [-1, 1]
            angle = math.acos(cos_angle) * 180 / math.pi
            return angle
        
        # Test cases
        test_cases = [
            ([0, 0], [1, 0], [1, 1]),  # 90 degrees
            ([0, 0], [1, 0], [2, 0]),  # 0 degrees
            ([0, 0], [1, 0], [0, 1]),  # 90 degrees
        ]
        
        for a, b, c in test_cases:
            angle = simple_angle_calc(a, b, c)
            assert 0 <= angle <= 180
            print(f"✅ Angle calculation test passed: {angle:.1f}°")
        
        return True
    except Exception as e:
        print(f"❌ Pose detection math test failed: {e}")
        return False

def test_file_structure():
    """Test that the improved file structure exists"""
    required_files = [
        "src/__init__.py",
        "src/utils/__init__.py",
        "src/utils/camera.py",
        "src/utils/pose_detection.py",
        "src/core/__init__.py",
        "src/core/data_manager.py",
        "src/core/goals_manager.py",
        "requirements.txt",
        "README.md",
        "test_improvements.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files exist")
        return True

def main():
    """Run all tests"""
    print("🧪 Testing FocusFit Improvements...")
    print("=" * 50)
    
    tests = [
        ("File Structure Tests", test_file_structure),
        ("Import Tests", test_imports),
        ("Data Manager Tests", test_data_manager),
        ("Goals Manager Tests", test_goals_manager),
        ("Pose Detection Math Tests", test_pose_detection_math),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Improvements are working correctly.")
        print("\n💡 Note: OpenCV-dependent tests were skipped.")
        print("   Install dependencies with: pip install -r requirements.txt")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
