from datetime import datetime, timedelta
import re
from typing import Optional


class DateParser:
    """Utility class for parsing and handling dates"""
    
    def __init__(self):
        self.today = datetime.now().date()
    
    def parse_relative_date(self, date_str: str) -> Optional[str]:
        """Parse relative dates like 'tomorrow', 'next week', etc."""
        date_str = date_str.lower().strip()
        
        if date_str in ['today']:
            return self.today.strftime('%Y-%m-%d')
        elif date_str in ['tomorrow']:
            return (self.today + timedelta(days=1)).strftime('%Y-%m-%d')
        elif date_str in ['next week']:
            days_ahead = 7 - self.today.weekday()
            return (self.today + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
        elif 'next' in date_str and 'monday' in date_str:
            days_ahead = 7 - self.today.weekday()
            return (self.today + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
        
        return None
    
    def format_time_slot(self, start_time: str, end_time: str) -> str:
        """Format time slot for display"""
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
        
        return f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}"