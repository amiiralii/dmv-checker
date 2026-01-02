#!/usr/bin/env python3
"""
NC DMV Appointment Checker

Automatically checks the NC DMV website for available appointments
and sends email notifications when slots open up.
"""

import logging
import smtplib
import sys
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

import config


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dmv_checker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def send_email(subject: str, body: str) -> bool:
    """Send email notification via Gmail SMTP."""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = config.EMAIL_FROM
        msg['To'] = config.EMAIL_TO

        # Create HTML version of the email
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #2e7d32;">🎉 DMV Appointment Available!</h2>
            <div style="background-color: #e8f5e9; padding: 20px; border-radius: 8px; margin: 20px 0;">
                {body.replace(chr(10), '<br>')}
            </div>
            <p style="color: #666; font-size: 14px;">
                <strong>Timestamp:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
                <strong>Quick Link:</strong><br>
                <a href="{config.DMV_URL}" style="color: #1976d2;">{config.DMV_URL}</a>
            </p>
            <p style="color: #999; font-size: 12px;">
                This is an automated message from your DMV Appointment Checker.
            </p>
        </body>
        </html>
        """

        text_part = MIMEText(body, 'plain')
        html_part = MIMEText(html_body, 'html')
        msg.attach(text_part)
        msg.attach(html_part)

        # Connect to Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(config.EMAIL_FROM, config.GMAIL_APP_PASSWORD)
            server.sendmail(config.EMAIL_FROM, config.EMAIL_TO, msg.as_string())

        logger.info(f"Email sent successfully to {config.EMAIL_TO}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False


def check_for_appointments() -> dict:
    """
    Check the NC DMV website for available appointments.
    
    Returns:
        dict with keys:
            - available: bool indicating if appointments are available
            - message: str with details
            - error: str if an error occurred (None otherwise)
    """
    result = {
        'available': False,
        'message': '',
        'error': None
    }

    logger.info("Starting DMV appointment check...")
    logger.info(f"Target location: {config.TARGET_LOCATION}")

    with sync_playwright() as p:
        try:
            # Launch browser (using Firefox for better macOS compatibility)
            browser = p.firefox.launch(headless=config.HEADLESS)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                permissions=[]  # Empty list = deny all permissions including geolocation
            )
            page = context.new_page()
            page.set_default_timeout(config.PAGE_TIMEOUT * 1000)

            # Navigate to DMV appointment page
            logger.info(f"Navigating to {config.DMV_URL}")
            page.goto(config.DMV_URL, wait_until='networkidle')
            time.sleep(3)  # Wait for any dynamic content
            
            # Log step 1
            with open('debug_log.txt', 'a') as f:
                f.write(f"=== DMV Check Log - {datetime.now()} ===\n\n")
                f.write("Step 1: Initial page loaded\n")
                f.write(f"URL: {page.url}\n\n")

            # Click "Make an Appointment" button first
            logger.info("Clicking Make an Appointment button...")
            make_appt_btn = page.get_by_role("button", name="Make an Appointment")
            make_appt_btn.click()
            
            # Wait for URL to change or new content to appear
            page.wait_for_load_state('networkidle')
            time.sleep(3)
            
            # Log step 2
            with open('debug_log.txt', 'a') as f:
                f.write("Step 2: Clicked 'Make an Appointment'\n")
                f.write(f"URL: {page.url}\n\n")

            # Look for the service type and click it
            logger.info(f"Looking for service: {config.SERVICE_TYPE}")
            
            # Find and click the Driver License service option - try multiple approaches
            service_clicked = False
            service_selectors = [
                page.get_by_text(config.SERVICE_TYPE, exact=False).first,
                page.get_by_text("Driver License", exact=False).first,
                page.get_by_text("First Time", exact=False).first,
                page.locator("[class*='service']").first,
            ]
            
            for selector in service_selectors:
                try:
                    if selector.is_visible(timeout=3000):
                        selector.click()
                        logger.info("Clicked on service type")
                        service_clicked = True
                        break
                except Exception as e:
                    logger.debug(f"Service selector failed: {e}")
                    continue
            
            if not service_clicked:
                with open('debug_log.txt', 'a') as f:
                    f.write("WARNING: Could not find service type\n\n")
                logger.warning("Could not find service type - may already be selected or page layout different")
            
            page.wait_for_load_state('networkidle')
            time.sleep(3)
            
            # Log step 3
            with open('debug_log.txt', 'a') as f:
                f.write("Step 3: After service selection\n")
                f.write(f"URL: {page.url}\n\n")

            # Now look for the target location
            logger.info(f"Searching for location: {config.TARGET_LOCATION}")
            

            # Find all divs with "disabled-unit" in their class
            # active_units = page.locator("div[class*='disabled-unit']").all()
            active_units = page.locator("div[class*='Activate-Unit']").all()
            logger.info(f"Found {len(active_units)} Activate-unit divs")
            
            # Log results to txt file
            with open('debug_log.txt', 'a') as f:
                f.write(f"Step 4: Found {len(active_units)} disabled-unit divs\n\n")
                
                for i, unit in enumerate(active_units):
                    try:
                        class_attr = unit.get_attribute("class")
                        inner_text = unit.inner_text()
                        if "Avent Ferry Shopping Center" in inner_text:
                            f.write(f"[{i+1}] Class: {class_attr}\n")
                            f.write(f"    Text: {inner_text}\n\n")
                            print(f"Found Raleigh West (Avent Ferry): {inner_text[:100]}...")
                            result['available'] = True
                    except Exception as e:
                        f.write(f"[{i+1}] Error: {e}\n")
                
                f.write("=" * 60 + "\n")

            browser.close()

        except PlaywrightTimeout as e:
            result['error'] = f"Timeout error: {e}"
            logger.error(result['error'])
            
        except Exception as e:
            result['error'] = f"Error during check: {e}"
            logger.error(result['error'])
            
            # Log error to txt file
            try:
                with open('debug_log.txt', 'a') as f:
                    f.write(f"ERROR: {e}\n")
                    f.write(f"URL at error: {page.url}\n\n")
            except:
                pass

    return result


def run_check():
    """Run a single appointment check and send notification if available."""
    logger.info("=" * 50)
    logger.info("DMV Appointment Check Started")
    logger.info("=" * 50)
    
    result = check_for_appointments()
    
    if result['error']:
        logger.error(f"Check failed with error: {result['error']}")
        return False
    
    if result['available']:
        logger.info("🎉 Appointment available! Sending notification...")
        send_email(
            subject="🚗 DMV Appointment Available - Raleigh West!",
            body=result['message']
        )
        return True
    else:
        logger.info(f"No appointments available. {result['message']}")
        return False


def run_continuous():
    """Run the checker continuously at configured intervals."""
    logger.info(f"Starting continuous monitoring (every {config.CHECK_INTERVAL} seconds)")
    logger.info("Press Ctrl+C to stop")
    
    while True:
        try:
            found = run_check()
            if found:
                logger.info("Appointment found and notification sent!")
                # Continue checking in case the user misses it
            
            logger.info(f"Next check in {config.CHECK_INTERVAL} seconds...")
            time.sleep(config.CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            logger.info("Stopping checker...")
            break


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        run_continuous()
    else:
        # Single check mode (for cron jobs)
        run_check()

