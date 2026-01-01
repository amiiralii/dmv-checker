#!/usr/bin/env python3
"""
Test script to verify email configuration is working.
Run this after setting up your Gmail App Password.
"""

import config
from dmv_checker import send_email

print("=" * 50)
print("Testing Email Configuration")
print("=" * 50)
print(f"From: {config.EMAIL_FROM}")
print(f"To: {config.EMAIL_TO}")
print(f"App Password: {'*' * 12 + config.GMAIL_APP_PASSWORD[-4:] if len(config.GMAIL_APP_PASSWORD) > 4 else 'NOT SET'}")
print("")

if config.GMAIL_APP_PASSWORD == "your-app-password-here":
    print("❌ ERROR: You need to set your Gmail App Password in config.py!")
    print("")
    print("Steps:")
    print("1. Go to https://myaccount.google.com/apppasswords")
    print("2. Generate a new App Password")
    print("3. Copy it to config.py (GMAIL_APP_PASSWORD)")
    exit(1)

print("Sending test email...")
success = send_email(
    subject="🧪 DMV Checker Test - Email Working!",
    body="""This is a test email from your DMV Appointment Checker.

If you're receiving this, your email configuration is working correctly!

The checker will notify you at this email address when appointments become available.

Configuration:
- Target Location: Raleigh West, Avent Ferry Shopping Center
- Service: Driver License - First Time

Happy driving! 🚗"""
)

if success:
    print("")
    print("✅ SUCCESS! Check your inbox for the test email.")
    print("Your DMV checker is ready to go!")
else:
    print("")
    print("❌ FAILED to send email. Check the error message above.")
    print("Common issues:")
    print("  - App Password is incorrect")
    print("  - 2-Step Verification is not enabled on your Google account")
    print("  - Less secure app access is blocked (use App Password instead)")

