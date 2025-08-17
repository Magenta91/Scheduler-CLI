import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json


class CalendarService:
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    def __init__(self):
        self.service = self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Calendar API"""
        creds = None
        
        # Load existing credentials
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Create credentials.json file first
                credentials_info = {
                    "installed": {
                        "client_id": os.getenv('GOOGLE_CLIENT_ID'),
                        "client_secret": os.getenv('GOOGLE_CLIENT_SECRET'),
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                        "redirect_uris": []
                    }
                }
                
                # Write credentials to file
                with open('credentials.json', 'w') as f:
                    json.dump(credentials_info, f, indent=2)
                
                # Use the credentials file
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                
                # Use local server authentication for desktop applications
                try:
                    print("Opening browser for authentication...")
                    print("If browser doesn't open automatically, copy the URL from the terminal")
                    # Use port 0 to let the system choose an available port
                    creds = flow.run_local_server(port=0, open_browser=True)
                except Exception as e:
                    print(f"Local server authentication failed: {e}")
                    print("Falling back to manual authentication...")
                    print("Please visit the URL below and enter the authorization code:")
                    creds = flow.run_console()
            
            # Save credentials for next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        return build('calendar', 'v3', credentials=creds)
    
    def find_available_slots(self, date: str, duration: int, attendees: List[str]) -> List[Dict]:
        """Find available time slots for the given date and attendees"""
        try:
            # Parse the date
            target_date = datetime.strptime(date, '%Y-%m-%d')
            
            # Define business hours (9 AM to 5 PM)
            start_time = target_date.replace(hour=9, minute=0, second=0, microsecond=0)
            end_time = target_date.replace(hour=17, minute=0, second=0, microsecond=0)
            
            # Get busy times for all attendees
            busy_times = self._get_busy_times(start_time, end_time, attendees)
            
            # Find free slots
            available_slots = []
            current_time = start_time
            
            while current_time + timedelta(minutes=duration) <= end_time:
                slot_end = current_time + timedelta(minutes=duration)
                
                # Check if this slot conflicts with any busy time
                is_free = True
                for busy_start, busy_end in busy_times:
                    if (current_time < busy_end and slot_end > busy_start):
                        is_free = False
                        break
                
                if is_free:
                    available_slots.append({
                        'start_time': current_time.isoformat(),
                        'end_time': slot_end.isoformat(),
                        'formatted_time': current_time.strftime('%I:%M %p')
                    })
                
                current_time += timedelta(minutes=30)  # Check every 30 minutes
            
            return available_slots
            
        except Exception as e:
            print(f"Error finding available slots: {e}")
            return []
    
    def _get_busy_times(self, start_time: datetime, end_time: datetime, attendees: List[str]) -> List[tuple]:
        """Get busy times for all attendees"""
        busy_times = []
        
        try:
            # Include the primary calendar
            calendars_to_check = ['primary']
            calendars_to_check.extend(attendees)
            
            for calendar_id in calendars_to_check:
                events_result = self.service.events().list(
                    calendarId=calendar_id,
                    timeMin=start_time.isoformat() + 'Z',
                    timeMax=end_time.isoformat() + 'Z',
                    singleEvents=True,
                    orderBy='startTime'
                ).execute()
                
                events = events_result.get('items', [])
                
                for event in events:
                    if 'dateTime' in event['start'] and 'dateTime' in event['end']:
                        event_start = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
                        event_end = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00'))
                        busy_times.append((event_start, event_end))
        
        except Exception as e:
            print(f"Error getting busy times: {e}")
        
        return busy_times
    
    def create_meeting(self, meeting_info: Dict, selected_slot: Dict) -> Dict:
        """Create a meeting in Google Calendar"""
        try:
            start_time = datetime.fromisoformat(selected_slot['start_time'])
            end_time = datetime.fromisoformat(selected_slot['end_time'])
            
            # Create Google Meet link
            conference_data = {
                'createRequest': {
                    'requestId': f"meet-{int(datetime.now().timestamp())}",
                    'conferenceSolutionKey': {'type': 'hangoutsMeet'}
                }
            }
            
            event = {
                'summary': meeting_info.get('title', 'Meeting'),
                'description': meeting_info.get('description', ''),
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'attendees': [{'email': email} for email in meeting_info.get('attendees', [])],
                'conferenceData': conference_data,
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            
            created_event = self.service.events().insert(
                calendarId='primary',
                body=event,
                conferenceDataVersion=1,
                sendUpdates='all'
            ).execute()
            
            return {
                'success': True,
                'event_id': created_event['id'],
                'event_link': created_event.get('htmlLink'),
                'meet_link': created_event.get('conferenceData', {}).get('entryPoints', [{}])[0].get('uri', 'No Meet link available')
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }