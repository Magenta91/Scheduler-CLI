import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import google.generativeai as genai
from services.calendar_service import CalendarService
from utils.date_parser import DateParser


class MeetingScheduler:
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.calendar_service = CalendarService()
        self.date_parser = DateParser()
    
    def parse_meeting_request(self, request: str) -> Dict:
        """Parse natural language meeting request using Gemini"""
        prompt = f"""
        Parse this meeting request and extract the following information in JSON format:
        - title: meeting title/subject
        - duration: duration in minutes (default 60)
        - attendees: list of email addresses
        - preferred_date: preferred date (YYYY-MM-DD format)
        - preferred_time: preferred time (HH:MM format, 24-hour)
        - description: meeting description/agenda
        
        Meeting request: "{request}"
        
        Return only valid JSON without any markdown formatting.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            print(f"Error parsing request: {e}")
            return {}
    
    def schedule_meeting(self, request: str) -> Dict:
        """Main method to schedule a meeting from natural language request"""
        # Parse the request
        meeting_info = self.parse_meeting_request(request)
        
        if not meeting_info:
            return {"error": "Could not parse meeting request"}
        
        # Get available slots
        slots = self.get_available_slots(
            meeting_info.get('preferred_date'),
            meeting_info.get('duration', 60),
            meeting_info.get('attendees', [])
        )
        
        if not slots:
            return {"error": "No available slots found"}
        
        return {
            "meeting_info": meeting_info,
            "suggested_slots": slots[:3]  # Return top 3 slots
        }
    
    def get_available_slots(self, preferred_date: str, duration: int, attendees: List[str]) -> List[Dict]:
        """Find available time slots"""
        if not preferred_date:
            preferred_date = datetime.now().strftime('%Y-%m-%d')
        
        return self.calendar_service.find_available_slots(
            preferred_date, duration, attendees
        )
    
    def confirm_meeting(self, meeting_info: Dict, selected_slot: Dict) -> Dict:
        """Create the meeting in Google Calendar"""
        return self.calendar_service.create_meeting(meeting_info, selected_slot)
