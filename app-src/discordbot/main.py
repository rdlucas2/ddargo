import os
import requests

# Retrieve the Discord webhook URL from environment variables
webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')

if not webhook_url:
    print("Error: Webhook URL is not set in the environment variables.")
    exit(1)

# Fetch a random cat fact
fact_response = requests.get("https://catfact.ninja/fact")

if fact_response.status_code == 200:
    fact_data = fact_response.json()
    cat_fact = fact_data.get("fact", "Couldn't fetch a cat fact right now.")
else:
    print(f"Failed to fetch cat fact. Status code: {fact_response.status_code}")
    cat_fact = "Couldn't fetch a cat fact right now."

# Define the message payload with the cat fact
data = {
    "content": cat_fact,
    "username": "Cat Facts Bot"  # Optional: Set a custom username for the bot
}

# Send the POST request to Discord webhook
response = requests.post(webhook_url, json=data)

# Check the response status
if response.status_code == 204:
    print("Message sent successfully!")
else:
    print(f"Failed to send message. Status code: {response.status_code}")