# DMV Appointment Checker Configuration
import os

# ============================================
# NC DMV SETTINGS
# ============================================
DMV_URL = "https://skiptheline.ncdot.gov/Webapp/Appointment/Index/a7ade79b-996d-4971-8766-97feb75254de"

# Service type to select
SERVICE_TYPE = "Driver License - First Time new driver over 18, new N.C. resident Real ID"

# Location to monitor for appointments
TARGET_LOCATION = "Raleigh West, Avent Ferry Shopping Center, 3231 Avent Ferry Road, Raleigh, NC 27606"

# ============================================
# EMAIL SETTINGS (uses env vars for GitHub Actions, fallback for local)
# ============================================
# It is NOT best practice to hardcode personal email addresses (even if not a password) in a public repo.
# Better: require EMAIL_TO and EMAIL_FROM to be set in the environment, remove defaults.
EMAIL_TO = os.environ.get("EMAIL_TO")
EMAIL_FROM = os.environ.get("EMAIL_FROM")

# Gmail App Password - reads from environment variable first
# WARNING: Never include actual passwords or secrets in source code, especially in a public repo!
# For safety, do NOT provide a default fallback here. Only read from the environment variable.
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

print(EMAIL_TO, EMAIL_FROM, GMAIL_APP_PASSWORD )
# ============================================
# CHECKER SETTINGS
# ============================================
# How long to wait for page elements (seconds)
PAGE_TIMEOUT = 30

# Run in headless mode (no browser window)
# Automatically True on GitHub Actions (CI=true), False locally for debugging
HEADLESS = os.environ.get("CI") == "true" or os.environ.get("HEADLESS", "false").lower() == "true"

# How often to check when running continuously (seconds)
# Default: 3600 = 1 hour
CHECK_INTERVAL = 3600

