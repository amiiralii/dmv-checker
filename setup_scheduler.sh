#!/bin/bash
# Setup script for DMV Appointment Checker scheduler

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_PATH=$(which python3)

echo "================================================"
echo "DMV Appointment Checker - Scheduler Setup"
echo "================================================"
echo ""
echo "This script will set up a cron job to run the checker."
echo "Script directory: $SCRIPT_DIR"
echo "Python path: $PYTHON_PATH"
echo ""

# Ask user for schedule preference
echo "How often do you want to check for appointments?"
echo "1) Every hour (recommended for best chances)"
echo "2) Every night at 11 PM"
echo "3) Every night at 6 AM"
echo "4) Every 30 minutes (aggressive)"
echo "5) Custom (enter your own cron schedule)"
echo ""
read -p "Enter choice (1-5): " choice

case $choice in
    1)
        CRON_SCHEDULE="0 * * * *"
        SCHEDULE_DESC="every hour"
        ;;
    2)
        CRON_SCHEDULE="0 23 * * *"
        SCHEDULE_DESC="every night at 11 PM"
        ;;
    3)
        CRON_SCHEDULE="0 6 * * *"
        SCHEDULE_DESC="every morning at 6 AM"
        ;;
    4)
        CRON_SCHEDULE="*/30 * * * *"
        SCHEDULE_DESC="every 30 minutes"
        ;;
    5)
        read -p "Enter cron schedule (e.g., '0 */2 * * *' for every 2 hours): " CRON_SCHEDULE
        SCHEDULE_DESC="custom schedule: $CRON_SCHEDULE"
        ;;
    *)
        echo "Invalid choice. Using default (every hour)."
        CRON_SCHEDULE="0 * * * *"
        SCHEDULE_DESC="every hour"
        ;;
esac

echo ""
echo "Setting up cron job to run $SCHEDULE_DESC..."

# Create a wrapper script that handles the virtual environment
cat > "$SCRIPT_DIR/run_checker.sh" << EOF
#!/bin/bash
cd "$SCRIPT_DIR"
source venv/bin/activate
python3 dmv_checker.py >> "$SCRIPT_DIR/cron.log" 2>&1
EOF

chmod +x "$SCRIPT_DIR/run_checker.sh"

# Create the cron entry
CRON_CMD="$CRON_SCHEDULE $SCRIPT_DIR/run_checker.sh"

# Check if cron job already exists
EXISTING_CRON=$(crontab -l 2>/dev/null | grep -F "dmv_checker.py")

if [ -n "$EXISTING_CRON" ]; then
    echo "Existing DMV checker cron job found. Removing old entry..."
    crontab -l 2>/dev/null | grep -v "dmv_checker.py" | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -

echo ""
echo "✅ Cron job installed successfully!"
echo ""
echo "Schedule: $SCHEDULE_DESC"
echo "Command: $CRON_CMD"
echo ""
echo "To view your cron jobs: crontab -l"
echo "To remove the job: crontab -e (and delete the line)"
echo ""
echo "Logs will be written to:"
echo "  - $SCRIPT_DIR/dmv_checker.log (detailed logs)"
echo "  - $SCRIPT_DIR/cron.log (cron execution logs)"

