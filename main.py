#!/usr/bin/env python3
"""
Meeting Scheduler CLI
A simple command-line interface for scheduling meetings using natural language.
"""

import os
import click
from dotenv import load_dotenv
from agents.meeting_scheduler import MeetingScheduler


# Load environment variables
load_dotenv()


@click.group()
def cli():
    """Meeting Scheduler - Schedule meetings using natural language"""
    pass


@cli.command()
@click.argument('request', required=True)
def schedule(request):
    """Schedule a meeting from natural language request
    
    Example: python main.py schedule "Schedule a team standup tomorrow at 10am with john@example.com and jane@example.com for 30 minutes"
    """
    try:
        scheduler = MeetingScheduler()
        result = scheduler.schedule_meeting(request)
        
        if 'error' in result:
            click.echo(f"❌ Error: {result['error']}")
            return
        
        meeting_info = result['meeting_info']
        slots = result['suggested_slots']
        
        click.echo(f"\n📅 Meeting: {meeting_info.get('title', 'Untitled Meeting')}")
        click.echo(f"⏱️  Duration: {meeting_info.get('duration', 60)} minutes")
        click.echo(f"👥 Attendees: {', '.join(meeting_info.get('attendees', []))}")
        
        if meeting_info.get('description'):
            click.echo(f"📝 Description: {meeting_info['description']}")
        
        click.echo(f"\n🕐 Available time slots:")
        for i, slot in enumerate(slots, 1):
            click.echo(f"  {i}. {slot['formatted_time']} ({slot['start_time'][:10]})")
        
        # Ask user to select a slot
        if slots:
            choice = click.prompt('\nSelect a time slot (1-3)', type=int)
            if 1 <= choice <= len(slots):
                selected_slot = slots[choice - 1]
                
                # Confirm the meeting
                click.echo(f"\n⏳ Creating meeting for {selected_slot['formatted_time']}...")
                confirmation = scheduler.confirm_meeting(meeting_info, selected_slot)
                
                if confirmation.get('success'):
                    click.echo("✅ Meeting created successfully!")
                    click.echo(f"🔗 Event link: {confirmation.get('event_link', 'N/A')}")
                    click.echo(f"📹 Meet link: {confirmation.get('meet_link', 'N/A')}")
                else:
                    click.echo(f"❌ Failed to create meeting: {confirmation.get('error', 'Unknown error')}")
            else:
                click.echo("❌ Invalid selection")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}")


@cli.command()
def test():
    """Test the connection to APIs"""
    click.echo("🔍 Testing API connections...")
    
    # Test environment variables
    required_vars = ['GEMINI_API_KEY', 'GOOGLE_CLIENT_ID', 'GOOGLE_CLIENT_SECRET']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        click.echo(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return
    
    click.echo("✅ Environment variables found")
    
    try:
        scheduler = MeetingScheduler()
        click.echo("✅ Gemini API connection successful")
        click.echo("✅ Calendar service initialized")
        click.echo("🎉 All systems ready!")
        
    except Exception as e:
        click.echo(f"❌ Error initializing services: {str(e)}")


@cli.command()
def example():
    """Show example usage"""
    click.echo("📖 Example usage:")
    click.echo("")
    click.echo("1. Schedule a meeting:")
    click.echo("   python main.py schedule \"Schedule a team standup tomorrow at 10am with john@example.com for 30 minutes\"")
    click.echo("")
    click.echo("2. Test API connections:")
    click.echo("   python main.py test")
    click.echo("")
    click.echo("3. Show this help:")
    click.echo("   python main.py example")


if __name__ == '__main__':
    cli()