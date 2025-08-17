# Meeting Scheduler CLI

A smart command-line interface for scheduling meetings using natural language processing. The application leverages Google's Gemini AI to parse meeting requests and integrates with Google Calendar to find available time slots and create meetings automatically.

## Features

- **Natural Language Processing**: Schedule meetings using plain English
- **Smart Scheduling**: Automatically finds available time slots
- **Google Calendar Integration**: Creates meetings with Google Meet links
- **Conflict Detection**: Checks attendee availability
- **Email Invitations**: Automatically sends calendar invites to attendees

## Architecture

### Project Structure

```
meeting-scheduler/
├── agents/
│   └── meeting_scheduler.py    # Main orchestration logic
├── services/
│   └── calendar_service.py     # Google Calendar API integration
├── utils/
│   └── date_parser.py          # Date/time parsing utilities
├── main.py                     # CLI interface
├── setup_oauth.py              # OAuth setup helper
├── .env                        # Environment variables
└── requirements.txt            # Python dependencies
```

### System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   CLI Interface │───▶│ Meeting Scheduler │───▶│ Calendar Service│
│    (main.py)    │    │     (Agent)       │    │   (Google API)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Gemini AI      │
                       │ (NLP Processing) │
                       └──────────────────┘
```

## Workflow

### 1. Request Processing
- User inputs natural language meeting request
- Gemini AI parses and extracts meeting details:
  - Title and description
  - Duration
  - Attendee email addresses
  - Preferred date and time

### 2. Availability Check
- System queries Google Calendar API
- Checks availability for all attendees
- Identifies conflicts and busy periods
- Generates list of available time slots

### 3. Meeting Creation
- User selects preferred time slot
- Creates Google Calendar event
- Generates Google Meet link
- Sends invitations to all attendees

## Installation

### Prerequisites
- Python 3.8+
- Google Cloud Project with Calendar API enabled
- OAuth 2.0 Desktop Application credentials

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd meeting-scheduler
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Google Cloud**
   - Create a Google Cloud Project
   - Enable Google Calendar API
   - Create OAuth 2.0 Desktop Application credentials
   - Download credentials JSON file as `credentials.json`

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys and credentials
   ```

5. **Set up Google OAuth credentials**
   ```bash
   # Download your OAuth credentials from Google Cloud Console
   # Rename the downloaded file to credentials.json
   # Or copy credentials.json.example to credentials.json and fill in your details
   cp credentials.json.example credentials.json
   ```

6. **Configure OAuth**
   ```bash
   python setup_oauth.py
   ```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_API_KEY=your_google_api_key
```

### OAuth Setup

The application uses OAuth 2.0 for Google Calendar access:
- First run requires browser authentication
- Subsequent runs use cached tokens
- Tokens are automatically refreshed when expired

## Usage

### Basic Commands

**Test API connections:**
```bash
python main.py test
```

**Schedule a meeting:**
```bash
python main.py schedule "Schedule a team standup tomorrow at 10am with john@company.com for 30 minutes"
```

**View examples:**
```bash
python main.py example
```

### Example Requests

The system understands various natural language formats:

```bash
# Basic meeting
python main.py schedule "Schedule a meeting with alice@company.com tomorrow at 2pm for 1 hour"

# Multiple attendees
python main.py schedule "Book a client call next Friday at 3pm with client@example.com and manager@company.com for 45 minutes"

# With description
python main.py schedule "Schedule a project review meeting tomorrow at 10am with team@company.com for 30 minutes to discuss Q4 goals"
```

## Components

### Meeting Scheduler Agent (`agents/meeting_scheduler.py`)
- **Purpose**: Main orchestration logic
- **Responsibilities**:
  - Coordinates between AI parsing and calendar services
  - Manages meeting workflow
  - Handles error scenarios

### Calendar Service (`services/calendar_service.py`)
- **Purpose**: Google Calendar API integration
- **Responsibilities**:
  - OAuth authentication management
  - Calendar event creation and management
  - Availability checking
  - Google Meet link generation

### Date Parser (`utils/date_parser.py`)
- **Purpose**: Date and time processing utilities
- **Responsibilities**:
  - Natural language date parsing
  - Time zone handling
  - Date format standardization

### CLI Interface (`main.py`)
- **Purpose**: Command-line user interface
- **Responsibilities**:
  - User input handling
  - Command routing
  - Output formatting
  - Interactive slot selection

## API Integration

### Google Calendar API
- **Scopes**: `https://www.googleapis.com/auth/calendar`
- **Authentication**: OAuth 2.0 Desktop Application flow
- **Features Used**:
  - Event creation and management
  - Freebusy queries
  - Conference data (Google Meet)

### Google Gemini AI
- **Model**: `gemini-1.5-flash`
- **Purpose**: Natural language processing
- **Input**: Raw meeting request text
- **Output**: Structured meeting data (JSON)

## Security

- **OAuth 2.0**: Secure authentication with Google services
- **Token Management**: Automatic token refresh and secure storage
- **API Keys**: Environment variable configuration
- **Scopes**: Minimal required permissions (Calendar access only)
- **Credential Protection**: All sensitive files are gitignored
- **Template Files**: Use .example files as templates for your credentials

### Important Security Notes

⚠️ **Never commit the following files to version control:**
- `.env` (contains API keys)
- `credentials.json` (contains OAuth credentials)
- `token.json` (contains access tokens)
- Any `client_secret_*.json` files

✅ **Safe to commit:**
- `.env.example` (template file)
- `credentials.json.example` (template file)
- `.gitignore` (protects sensitive files)

## Error Handling

The application includes comprehensive error handling:
- **API Failures**: Graceful degradation and user feedback
- **Authentication Issues**: Clear guidance for re-authentication
- **Invalid Requests**: Helpful error messages and suggestions
- **Network Issues**: Retry logic and timeout handling

## Development

### Adding New Features

1. **New AI Capabilities**: Extend prompts in `meeting_scheduler.py`
2. **Calendar Features**: Add methods to `calendar_service.py`
3. **CLI Commands**: Add new commands in `main.py`
4. **Utilities**: Add helper functions in `utils/`

### Testing

```bash
# Test API connections
python main.py test

# Test with sample data
python main.py schedule "Test meeting tomorrow at 10am with test@example.com for 30 minutes"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.