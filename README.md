# 🚗 NC DMV Appointment Checker

A friendly little bot that monitors the NC DMV website for available appointments and emails you the moment one opens up. Runs automatically on GitHub Actions – even while you sleep!

## ✨ Features

- ✅ Checks NC DMV "Skip the Line" website every hour
- ✅ Monitors Raleigh West (Avent Ferry) location
- ✅ Sends instant email notifications when appointments are available
- ✅ Runs 24/7 for free on GitHub Actions
- ✅ No server required – just fork and configure!

---

## 🚀 Quick Setup (GitHub Actions)

### Step 1: Fork This Repository

Click the **Fork** button at the top right of this page.

### Step 2: Set Up Gmail App Password

To send email notifications, you need a Gmail App Password:

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** if not already enabled
3. Go to [App Passwords](https://myaccount.google.com/apppasswords)
4. Select app: **Mail**, device: **Other** (name it "DMV Checker")
5. Click **Generate** and copy the 16-character password

### Step 3: Add GitHub Secrets

In your forked repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret** and add these three secrets:

| Name | Value |
|------|-------|
| `EMAIL_TO` | Your email address (where to receive notifications) |
| `EMAIL_FROM` | Your Gmail address (sender) |
| `GMAIL_APP_PASSWORD` | The 16-character app password from Step 2 |

### Step 4: Enable GitHub Actions

1. Go to the **Actions** tab in your repository
2. Click **"I understand my workflows, go ahead and enable them"**
3. Click on **"DMV Appointment Check"** workflow
4. Click **"Run workflow"** to test it manually

That's it! 🎉 The checker will now run automatically every hour.

---

## ⚙️ Configuration

Edit `config.py` to customize:

| Setting | Description | Default |
|---------|-------------|---------|
| `TARGET_LOCATION` | DMV office to monitor | Raleigh West (Avent Ferry) |
| `SERVICE_TYPE` | Type of appointment | First Time Driver License |
| `CHECK_INTERVAL` | Seconds between checks (continuous mode) | 3600 (1 hour) |

---

## 💻 Local Development (Optional)

If you want to run the checker on your own computer:

### Install Dependencies

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/dmv-checker.git
cd dmv-checker

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Firefox browser for Playwright
playwright install firefox
```

### Set Environment Variables

```bash
export EMAIL_TO="your-email@gmail.com"
export EMAIL_FROM="your-email@gmail.com"
export GMAIL_APP_PASSWORD="your-app-password"
```

### Run the Checker

```bash
# Single check
python dmv_checker.py

# Continuous monitoring (checks every hour)
python dmv_checker.py --continuous
```

---

## 📁 Project Structure

```
dmv-checker/
├── .github/workflows/
│   └── dmv_check.yml    # GitHub Actions workflow
├── config.py            # Configuration settings
├── dmv_checker.py       # Main checker script
├── requirements.txt     # Python dependencies
├── .gitignore          # Files to ignore in git
└── README.md           # This file
```

---

## 🔧 How It Works

1. **GitHub Actions** runs the script every hour (configurable via cron)
2. The script launches a headless Firefox browser using **Playwright**
3. It navigates to the NC DMV appointment page
4. Clicks through to find available appointments at your target location
5. If an appointment is available, it sends you an email notification

---

## 🛠️ Troubleshooting

### Email not sending
- Verify your `GMAIL_APP_PASSWORD` secret is set correctly (no extra spaces)
- Make sure 2-Step Verification is enabled on your Google account
- Check the Actions log for error messages

### "Headless browser" errors on GitHub Actions
- The `HEADLESS` setting automatically enables on GitHub Actions (via `CI=true`)
- If running locally, set `export HEADLESS=true` for headless mode

### Browser crashes on macOS (Apple Silicon)
- The script uses Firefox instead of Chromium for better compatibility
- If issues persist, try: `playwright install firefox`

### Workflow not running on schedule
- GitHub Actions scheduled workflows can be delayed during high-demand periods
- New repos may take up to an hour for schedules to activate
- You can always trigger manually from the Actions tab

---

## 📧 Email Notification Example

When an appointment becomes available:

```
Subject: 🚗 DMV Appointment Available - Raleigh West!

🎉 DMV Appointment Available!

Found Raleigh West (Avent Ferry Shopping Center)...

Quick Link: https://skiptheline.ncdot.gov/...

⚠️ Book fast – appointments fill up quickly!
```

---

## 📝 Notes

- The NC DMV website requires JavaScript, which is why we use Playwright
- Appointments can fill up within minutes, so hourly checks are recommended
- GitHub Actions is free for public repositories

---

## 🤝 Contributing

Found a bug or want to add a feature? PRs are welcome!

---

Made with ❤️ to help you get your driver's license faster!
