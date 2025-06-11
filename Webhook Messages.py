import requests
import shutil
from pyfiglet import Figlet
from datetime import datetime, timezone
import getpass 

# Your updated webhooks dictionary
webhooks = {
    "1": ("Name", "Webhook URL"),
    "2": ("Name", "Webhook URL"),
    "3": ("Name", "Webhook URL"),
    "4": ("Name", "Webhook URL"),
}

# Log webhook URL — replace this with your actual logs webhook URL
log_webhook_url = "Webhook URL"

# ANSI colors
PURPLE = "\033[95m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def print_centered(text):
    columns = shutil.get_terminal_size().columns
    for line in text.split("\n"):
        print(line.center(columns))

def print_banner():
    f = Figlet(font='slant')
    banner_text = f.renderText('Webhook Messenger')
    print(PURPLE, end="")
    print_centered(banner_text)
    print(RESET, end="")

def send_message(webhook_url, content):
    data = {"content": content}
    response = requests.post(webhook_url, json=data)
    return response.status_code == 204

def send_log(webhook_name, webhook_url, message_content):
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    short_url = webhook_url[:30] + "..." if len(webhook_url) > 33 else webhook_url

    embed = {
        "title": "Message Sent",
        "color": 0x1abc9c,
        "fields": [
            {"name": "Webhook Name", "value": webhook_name, "inline": True},
            {"name": "Webhook URL", "value": short_url, "inline": True},
            {"name": "Message Content", "value": message_content, "inline": False},
        ],
        "timestamp": timestamp,
        "footer": {"text": "Webhook Messenger Logger"}
    }

    payload = {"embeds": [embed]}
    response = requests.post(log_webhook_url, json=payload)
    if response.status_code != 204:
        print(f"{RED}Failed to send log message. Status code: {response.status_code}{RESET}")

def send_startup_log():
    username = getpass.getuser()
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    embed = {
        "title": "Python File Executed",
        "color": 0x3498db,
        "fields": [
            {"name": "User", "value": username, "inline": True},
            {"name": "Event", "value": "Webhook Messenger was opened", "inline": False},
        ],
        "timestamp": timestamp,
        "footer": {"text": "Webhook Messenger Logger"}
    }

    payload = {"embeds": [embed]}
    response = requests.post(log_webhook_url, json=payload)
    if response.status_code != 204:
        print(f"{RED}Failed to send startup log message. Status code: {response.status_code}{RESET}")

def main():
    print_banner()
    send_startup_log()

    while True:
        print("Select a webhook to send a message to:")
        columns = shutil.get_terminal_size().columns

        for key, (name, _) in webhooks.items():
            text = f"{key}. {name}"
            print(GREEN + text.center(columns) + RESET)

        print(GREEN + "q. Quit".center(columns) + RESET)

        choice = input("Your choice: ").strip()
        if choice.lower() == 'q':
            print("Exiting...")
            break

        if choice not in webhooks:
            print("Invalid choice. Try again.\n")
            continue

        webhook_name, url = webhooks[choice]
        message = input("Enter your message: ").strip()
        if not message:
            print("Message cannot be empty. Try again.\n")
            continue

        if send_message(url, message):
            print(GREEN + "Message sent successfully!\n" + RESET)
            send_log(webhook_name, url, message)
        else:
            print(RED + "Failed to send message.\n" + RESET)

if __name__ == "__main__":
    main()
