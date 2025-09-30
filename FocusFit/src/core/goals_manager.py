import json
import os
from datetime import datetime, timedelta
from typing import Dict, Tuple

class GoalsManager:
    """Enhanced goals management with better data handling"""
    
    def __init__(self, goals_file: str):
        self.goals_file = goals_file
        self.DAILY_GOAL_REPS = 50
        self.WEEKLY_GOAL_CHALLENGES = 5
        self.goals_data = self.load_goals()
    
    def load_goals(self) -> Dict:
        """Load goals data with error handling"""
        try:
            if os.path.exists(self.goals_file):
                with open(self.goals_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading goals: {e}")
        return {}
    
    def save_goals(self) -> bool:
        """Save goals data with error handling"""
        try:
            with open(self.goals_file, 'w') as f:
                json.dump(self.goals_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving goals: {e}")
            return False
    
    def get_today(self) -> str:
        """Get today's date string"""
        return datetime.now().strftime('%Y-%m-%d')
    
    def get_week(self) -> str:
        """Get current week string"""
        now = datetime.now()
        return f"{now.year}-W{now.isocalendar()[1]}"
    
    def get_daily_progress(self) -> int:
        """Get today's rep progress"""
        today = self.get_today()
        return self.goals_data.get(today, {}).get("reps", 0)
    
    def get_weekly_progress(self) -> int:
        """Get this week's challenge progress"""
        week = self.get_week()
        return self.goals_data.get(week, {}).get("challenges", 0)
    
    def update_progress(self, reps: int) -> bool:
        """Update progress with new reps and challenge"""
        try:
            today = self.get_today()
            week = self.get_week()
            
            # Update daily reps
            if today not in self.goals_data:
                self.goals_data[today] = {"reps": 0}
            self.goals_data[today]["reps"] += reps
            
            # Update weekly challenges
            if week not in self.goals_data:
                self.goals_data[week] = {"challenges": 0}
            self.goals_data[week]["challenges"] += 1
            
            return self.save_goals()
        except Exception as e:
            print(f"Error updating progress: {e}")
            return False
    
    def get_progress_percentage(self) -> Tuple[float, float]:
        """Get daily and weekly progress percentages"""
        daily_progress = min(self.get_daily_progress(), self.DAILY_GOAL_REPS)
        weekly_progress = min(self.get_weekly_progress(), self.WEEKLY_GOAL_CHALLENGES)
        
        daily_percent = (daily_progress / self.DAILY_GOAL_REPS) * 100
        weekly_percent = (weekly_progress / self.WEEKLY_GOAL_CHALLENGES) * 100
        
        return daily_percent, weekly_percent
    
    def is_daily_goal_achieved(self) -> bool:
        """Check if daily goal is achieved"""
        return self.get_daily_progress() >= self.DAILY_GOAL_REPS
    
    def is_weekly_goal_achieved(self) -> bool:
        """Check if weekly goal is achieved"""
        return self.get_weekly_progress() >= self.WEEKLY_GOAL_CHALLENGES
    
    def get_weekly_stats(self) -> Dict:
        """Get weekly statistics"""
        week = self.get_week()
        week_data = self.goals_data.get(week, {})
        
        # Calculate daily breakdown for the week
        daily_breakdown = {}
        for i in range(7):
            date = datetime.now() - timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            daily_breakdown[date_str] = self.goals_data.get(date_str, {}).get("reps", 0)
        
        return {
            "total_reps": week_data.get("reps", 0),
            "total_challenges": week_data.get("challenges", 0),
            "daily_breakdown": daily_breakdown
        }

