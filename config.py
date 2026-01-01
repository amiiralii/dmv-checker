# DMV Appointment Checker Configuration

# ============================================
# NC DMV SETTINGS
# ============================================
DMV_URL = "https://skiptheline.ncdot.gov/Webapp/Appointment/Index/a7ade79b-996d-4971-8766-97feb75254de"

# Service type to select
SERVICE_TYPE = "Driver License - First Time new driver over 18, new N.C. resident Real ID"

# Location to monitor for appointments
TARGET_LOCATION = "Raleigh West, Avent Ferry Shopping Center, 3231 Avent Ferry Road, Raleigh, NC 27606"

# ============================================
# EMAIL SETTINGS
# ============================================
EMAIL_TO = "amiraliraygan@gmail.com"
EMAIL_FROM = "amiraliraygan@gmail.com"

# Gmail App Password (you need to generate this - see README)
# DO NOT use your regular Gmail password!
GMAIL_APP_PASSWORD = "tthu fkac uemr zywz" 

# ============================================
# CHECKER SETTINGS
# ============================================
# How long to wait for page elements (seconds)
PAGE_TIMEOUT = 30

# Run in headless mode (no browser window)
HEADLESS = False

# How often to check when running continuously (seconds)
# Default: 3600 = 1 hour
CHECK_INTERVAL = 3600

