import requests
import shutil
from pyfiglet import Figlet
from datetime import datetime, timezone
import getpass  # To get the system username
import time

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
    banner_text = f.renderText('Webhook Tool')
    print(PURPLE, end="")
    print_centered(banner_text)
    print(RESET, end="")

def send_message(webhook_url, content):
    data = {"content": content}
    response = requests.post(webhook_url, json=data)
    return response

def delete_webhook(webhook_url):
    response = requests.delete(webhook_url)
    return response

def main():
    print_banner()
    print(GREEN + "Press Ctrl+C at any time to stop the program.\n" + RESET)

    webhook_url = input("Enter the webhook URL: ").strip()
    if not webhook_url.startswith("https://discord.com/api/webhooks/"):
        print(RED + "Invalid webhook URL format." + RESET)
        return

    print("What do you want to do?")
    print("1. Spam the webhook")
    print("2. Delete the webhook")
    action = input("Enter 1 or 2: ").strip()

    if action == "2":
        confirm = input(RED + "Are you sure you want to DELETE this webhook? (y/n): " + RESET).strip().lower()
        if confirm == "y":
            response = delete_webhook(webhook_url)
            if response.status_code == 204:
                print(GREEN + "Webhook deleted successfully!" + RESET)
            else:
                print(RED + f"Failed to delete webhook. Status code: {response.status_code}" + RESET)
        else:
            print("Deletion cancelled.")
        return

    elif action == "1":
        message = input("Enter the message to spam: ").strip()
        if not message:
            print(RED + "Message cannot be empty." + RESET)
            return

        try:
            count = int(input("Enter how many times to send the message: ").strip())
            if count <= 0:
                print(RED + "Count must be a positive integer." + RESET)
                return
        except ValueError:
            print(RED + "Invalid number." + RESET)
            return

        cooldown_input = input("Enter cooldown between messages in milliseconds (or 0 for no cooldown): ").strip()
        try:
            cooldown_ms = int(cooldown_input)
            if cooldown_ms < 0:
                print(RED + "Cooldown cannot be negative." + RESET)
                return
        except ValueError:
            print(RED + "Invalid cooldown." + RESET)
            return

        print(GREEN + f"Starting to spam webhook {count} times with cooldown {cooldown_ms}ms...\n" + RESET)

        for i in range(count):
            response = send_message(webhook_url, message)
            if response.status_code == 204:
                print(GREEN + f"[{i+1}/{count}] Message sent successfully!" + RESET)
            elif response.status_code == 429:
                retry_after = response.json().get("retry_after", 0) / 1000
                print(RED + f"Rate limited! Retry after {retry_after:.2f} seconds." + RESET)
                time.sleep(retry_after)
                # After waiting retry sending this message again
                continue
            else:
                print(RED + f"Failed to send message. Status code: {response.status_code}" + RESET)
                break

            if cooldown_ms > 0:
                time.sleep(cooldown_ms / 1000)

        print(GREEN + "Done!" + RESET)

    else:
        print(RED + "Invalid action choice." + RESET)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n" + RED + "Program stopped by user." + RESET)
