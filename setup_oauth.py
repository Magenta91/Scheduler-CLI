#!/usr/bin/env python3
"""
OAuth Setup Helper
This script helps you configure the Google Cloud Console for the meeting scheduler.
"""

import click


@click.command()
def setup():
    """Guide for setting up Google OAuth"""
    click.echo("🔧 Google OAuth Setup Guide")
    click.echo("=" * 50)
    click.echo("")
    click.echo("1. Go to Google Cloud Console: https://console.cloud.google.com/")
    click.echo("2. Create a new project or select an existing one")
    click.echo("3. Enable the Google Calendar API:")
    click.echo("   - Go to APIs & Services > Library")
    click.echo("   - Search for 'Google Calendar API'")
    click.echo("   - Click Enable")
    click.echo("")
    click.echo("4. Create OAuth 2.0 credentials:")
    click.echo("   - Go to APIs & Services > Credentials")
    click.echo("   - Click 'Create Credentials' > 'OAuth 2.0 Client IDs'")
    click.echo("   - Choose 'Desktop application'")
    click.echo("   - Add these redirect URIs:")
    click.echo("     • http://localhost:8080")
    click.echo("     • http://localhost")
    click.echo("     • urn:ietf:wg:oauth:2.0:oob")
    click.echo("")
    click.echo("5. Download the credentials JSON file")
    click.echo("6. Copy the client_id and client_secret to your .env file")
    click.echo("")
    click.echo("✅ After setup, run: python main.py test")


if __name__ == '__main__':
    setup()