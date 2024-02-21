import os
import time
from datetime import datetime

# Configuration
TARGET_IP = "192.168.1.100"  # Example IP, change to your smart plug's IP
CHECK_INTERVAL = 60  # Seconds between checks
EMAIL_SENDER = "your_email@example.com"
EMAIL_PASSWORD = "your_password"
EMAIL_RECIPIENT = "recipient_email@example.com"

def is_ip_reachable(ip):
    """Check if an IP address is reachable by pinging it."""
    response = os.system(f"ping -n 1 {ip}")
    return response == 0

def send_email_notification():
    """Send an email notification (placeholder function)."""
    # Placeholder for sending an email, you should implement this according to your email provider (e.g., using smtplib)
    print(f"[{datetime.now()}] Email notification sent to {EMAIL_RECIPIENT} (not really, implement this function).")

def main():
    while True:
        if not is_ip_reachable(TARGET_IP):
            print(f"[{datetime.now()}] WARNING: IP {TARGET_IP} is not reachable. Sending email notification.")
            send_email_notification()
        else:
            print(f"[{datetime.now()}] IP {TARGET_IP} is reachable.")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
