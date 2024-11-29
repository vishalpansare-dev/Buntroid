import subprocess


def send_email(subject, recipient, body):
    applescript = f"""
    tell application "Mail"
        set newMessage to make new outgoing message with properties {{
            subject:"{subject}",
            content:"{body}",
            visible:true
        }}
        make new to recipient at newMessage with properties {{address:"{recipient}"}}
        send newMessage
    end tell
    """

    # Print the AppleScript for debugging
    print("AppleScript to be executed:", applescript)

    # Run the AppleScript command via subprocess
    subprocess.run(["osascript", "-e", applescript])


def read_inbox():
    applescript = """
    tell application "Mail"
        set theMessages to messages of inbox
        set theSubject to subject of item 1 of theMessages
        set theSender to sender of item 1 of theMessages
        return "Subject: " & theSubject & " | Sender: " & theSender
    end tell
    """

    # Run the AppleScript command to read the inbox
    result = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)
    return result.stdout.strip()


def delete_email():
    applescript = """
    tell application "Mail"
        set theMessages to messages of inbox
        delete item 1 of theMessages
    end tell
    """

    # Run the AppleScript command to delete an email
    subprocess.run(["osascript", "-e", applescript])


if __name__ == "__main__":
    # Example usage:
    send_email("Test Email", "recipient@example.com", "Hello, this is a test email from Python!")
