import imaplib
import email
import threading
import time
from utils.logger import log
from assistant.speech.text_to_speech import speak
import smtplib
from email.mime.text import MIMEText
import os
import json

# Load configuration
with open("config.json", "r") as config_file:
    config = json.load(config_file)

EMAIL_USERNAME = os.getenv("EMAIL_USERNAME", config.get("email", {}).get("username"))
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", config.get("email", {}).get("password"))
IMAP_SERVER = config.get("email", {}).get("imap_server", "imap.gmail.com")
SMTP_SERVER = config.get("email", {}).get("smtp_server", "smtp.gmail.com")
CHECK_INTERVAL = config.get("email", {}).get("check_interval", 60)  # in seconds


def send_email_alert(subject):
    try:
        msg = MIMEText(f"You have a new email: {subject}")
        msg["Subject"] = "New Email Notification"
        msg["From"] = EMAIL_USERNAME
        msg["To"] = EMAIL_USERNAME

        with smtplib.SMTP(SMTP_SERVER, 587) as server:
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USERNAME, EMAIL_USERNAME, msg.as_string())

        log("Email alert sent successfully.", "info")
    except Exception as e:
        log(f"Failed to send email alert: {e}", "error")


def check_email(shutdown_event):
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        mail.select("inbox")

        while not shutdown_event.is_set():
            status, messages = mail.search(None, "UNSEEN")
            unread_emails = []

            for num in messages[0].split():
                status, msg_data = mail.fetch(num, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject = msg["subject"]
                        unread_emails.append(subject)
                        log(f"New email found: {subject}", "info")
                        speak(f"You have a new email: {subject}")
                        send_email_alert(subject)

            if not unread_emails:
                log("No new emails found.", "info")

            time.sleep(CHECK_INTERVAL)

    except Exception as e:
        log(f"Error checking email: {e}", "error")


def start_email_checker(shutdown_event):
    log("Starting email checker thread...", "info")
    email_thread = threading.Thread(target=check_email, args=(shutdown_event,), daemon=True)
    email_thread.start()
    log("Email checker thread started successfully.", "info")

if __name__ == "__main__":
    # Create a shutdown event to manage graceful shutdown
    shutdown_event = threading.Event()
    start_email_checker(shutdown_event)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        shutdown_event.set()  # Signal threads to stop gracefully
