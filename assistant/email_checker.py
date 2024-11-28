import imaplib
import email


def check_emails(email_address, password, imap_server="imap.gmail.com", folder="INBOX"):
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_address, password)
        mail.select(folder)

        _, data = mail.search(None, "UNSEEN")
        email_ids = data[0].split()

        messages = []
        for e_id in email_ids:
            _, msg_data = mail.fetch(e_id, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            subject = msg["subject"]
            from_ = msg["from"]
            messages.append(f"From: {from_}, Subject: {subject}")

        mail.logout()
        return messages if messages else ["No new emails."]
    except Exception as e:
        return [f"Error: {e}"]
