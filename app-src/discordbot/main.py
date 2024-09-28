import os
import requests

# Retrieve the Discord webhook URL from environment variables
webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')

if not webhook_url:
    print("Error: Webhook URL is not set in the environment variables.")
    exit(1)

# Define the message payload
data = {
    "content": "Hello, Discord! This is a scheduled test message.",
    "username": "Webhook Bot"  # Optional: Set a custom username for the bot
}

# Send the POST request
response = requests.post(webhook_url, json=data)

# Check the response status
if response.status_code == 204:
    print("Message sent successfully!")
else:
    print(f"Failed to send message. Status code: {response.status_code}")