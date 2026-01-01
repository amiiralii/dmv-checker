# 🚗 NC DMV Appointment Checker

Automatically monitors the NC DMV website for available driving test appointments and sends email notifications when slots open up.

## 📋 Features

- ✅ Checks NC DMV "Skip the Line" website for appointments
- ✅ Monitors specific location (Raleigh West - Avent Ferry)
- ✅ Sends instant email notifications when appointments are available
- ✅ Runs automatically via cron job
- ✅ Detailed logging for troubleshooting

## 🚀 Quick Setup

### Step 1: Install Python Dependencies

```bash
cd /Users/amirali/Desktop/dmv-checker

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### Step 2: Set Up Gmail App Password

To send emails from Gmail, you need to create an "App Password":

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** if not already enabled
3. Go to [App Passwords](https://myaccount.google.com/apppasswords)
4. Select "Mail" and "Mac" (or your device)
5. Click **Generate**
6. Copy the 16-character password (looks like: `xxxx xxxx xxxx xxxx`)

### Step 3: Configure the Checker

Edit `config.py` and add your Gmail App Password:

```python
GMAIL_APP_PASSWORD = "xxxx xxxx xxxx xxxx"  # Your 16-character app password
```

### Step 4: Test the Checker

Run a single check to make sure everything works:

```bash
source venv/bin/activate
python3 dmv_checker.py
```

You should see output like:
```
2024-01-15 10:30:00 - INFO - Starting DMV appointment check...
2024-01-15 10:30:05 - INFO - Navigating to NC DMV website...
...
```

### Step 5: Set Up Automatic Scheduling

Run the scheduler setup script:

```bash
chmod +x setup_scheduler.sh
./setup_scheduler.sh
```

This will let you choose how often to check (recommended: every hour).

## 📁 File Structure

```
dmv-checker/
├── config.py           # Configuration (email, location, etc.)
├── dmv_checker.py      # Main checker script
├── requirements.txt    # Python dependencies
├── setup_scheduler.sh  # Cron job setup script
├── README.md          # This file
├── venv/              # Python virtual environment (created during setup)
├── dmv_checker.log    # Detailed logs
└── cron.log           # Cron execution logs
```

## ⚙️ Configuration Options

Edit `config.py` to customize:

| Setting | Description | Default |
|---------|-------------|---------|
| `TARGET_LOCATION` | DMV office to monitor | Raleigh West |
| `SERVICE_TYPE` | Type of appointment | First Time Driver License |
| `EMAIL_TO` | Your email for notifications | amiraliraygan@gmail.com |
| `HEADLESS` | Run browser without window | True |
| `CHECK_INTERVAL` | Seconds between checks (continuous mode) | 3600 |

## 🔧 Usage

### Single Check (for cron jobs)
```bash
python3 dmv_checker.py
```

### Continuous Monitoring
```bash
python3 dmv_checker.py --continuous
```

### View Logs
```bash
tail -f dmv_checker.log
```

## 🛠️ Troubleshooting

### "No appointments available" but website shows availability
- The website might have changed its structure
- Check `debug_screenshot.png` if it was created
- Try running with `HEADLESS = False` in config to see the browser

### Email not sending
- Verify your Gmail App Password in `config.py`
- Make sure 2-Step Verification is enabled on your Google account
- Check for error messages in `dmv_checker.log`

### Cron job not running
- Check cron logs: `tail -f cron.log`
- Verify the job exists: `crontab -l`
- Make sure the virtual environment is set up correctly

### Browser errors
- Reinstall Playwright: `playwright install chromium`
- Update Playwright: `pip install --upgrade playwright`

## 📧 Email Notification Example

When an appointment becomes available, you'll receive an email like:

```
Subject: 🚗 DMV Appointment Available - Raleigh West!

🎉 DMV Appointment Available!

APPOINTMENT AVAILABLE at Raleigh West, Avent Ferry Shopping Center...

The appointment button is now CLICKABLE.

Book immediately at: https://skiptheline.ncdot.gov/...

⚠️ Remember: You need to confirm within 15 minutes of booking!
```

## 🛑 Stop the Checker

To remove the cron job:
```bash
crontab -e
# Delete the line containing dmv_checker.py
# Save and exit
```

## 📝 Notes

- The NC DMV website requires JavaScript, which is why we use Playwright instead of simple HTTP requests
- Appointments can fill up within minutes, so checking hourly (or more frequently) is recommended
- Remember to confirm your appointment within 15 minutes of booking, then again 4 days before!

---

Made with ❤️ to help you get your driver's license faster!

