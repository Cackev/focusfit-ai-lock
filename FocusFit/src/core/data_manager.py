import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class DataManager:
    """Enhanced data management with backup functionality and validation"""
    
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.backup_dir = "backups"
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def load_data(self) -> Dict:
        """Load data with error handling and validation"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                
                # Validate data structure
                if not isinstance(data, dict):
                    raise ValueError("Invalid data format")
                
                # Ensure required keys exist
                if "history" not in data:
                    data["history"] = []
                if "custom_challenges" not in data:
                    data["custom_challenges"] = []
                
                return data
            else:
                # File doesn't exist, return default structure
                return {"history": [], "custom_challenges": []}
        except Exception as e:
            print(f"Error loading data: {e}")
            # Return default structure
            return {"history": [], "custom_challenges": []}
    
    def save_data(self, data: Dict) -> bool:
        """Save data with backup creation"""
        try:
            # Create backup if file exists
            if os.path.exists(self.data_file):
                backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                backup_path = os.path.join(self.backup_dir, backup_name)
                os.rename(self.data_file, backup_path)
                print(f"Backup created: {backup_path}")
            
            # Save new data
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def add_history_entry(self, challenge: str, reps: int) -> bool:
        """Add a new history entry with timestamp"""
        try:
            data = self.load_data()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            entry = f"{timestamp} | {challenge} | {reps} reps"
            data["history"].append(entry)
            
            # Keep only last 10 entries
            if len(data["history"]) > 10:
                data["history"] = data["history"][-10:]
            
            return self.save_data(data)
        except Exception as e:
            print(f"Error adding history entry: {e}")
            return False
    
    def add_custom_challenge(self, name: str, icon: str) -> bool:
        """Add a custom challenge"""
        try:
            data = self.load_data()
            data["custom_challenges"].append([name, icon])
            return self.save_data(data)
        except Exception as e:
            print(f"Error adding custom challenge: {e}")
            return False
    
    def get_history(self) -> List[str]:
        """Get history entries"""
        data = self.load_data()
        return data.get("history", [])
    
    def get_custom_challenges(self) -> List[List[str]]:
        """Get custom challenges"""
        data = self.load_data()
        return data.get("custom_challenges", [])
    
    def export_data(self, export_path: str) -> bool:
        """Export data to a file"""
        try:
            data = self.load_data()
            with open(export_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting data: {e}")
            return False

