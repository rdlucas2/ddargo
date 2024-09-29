import os
import requests

# Retrieve the Discord webhook URL from environment variables
webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')

if not webhook_url:
    print("Error: Webhook URL is not set in the environment variables.")
    exit(1)

# Fetch a random Chuck Norris joke
joke_response = requests.get("https://api.chucknorris.io/jokes/random")

if joke_response.status_code == 200:
    joke_data = joke_response.json()
    joke = joke_data.get("value", "Couldn't fetch a joke right now.")
else:
    print(f"Failed to fetch joke. Status code: {joke_response.status_code}")
    joke = "Couldn't fetch a joke right now."

# Define the message payload with the Chuck Norris joke
data = {
    "content": joke,
    "username": "Chuck Norris Bot"  # Optional: Set a custom username for the bot
}

# Send the POST request to Discord webhook
response = requests.post(webhook_url, json=data)

# Check the response status
if response.status_code == 204:
    print("Message sent successfully!")
else:
    print(f"Failed to send message. Status code: {response.status_code}")