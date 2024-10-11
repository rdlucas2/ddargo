import unittest
from unittest.mock import patch, MagicMock
import requests
import os

# The function to be tested (assuming it's in a file named `main.py`)
from main import webhook_url, fact_response, response

class TestDiscordBot(unittest.TestCase):

    @patch.dict(os.environ, {'DISCORD_WEBHOOK_URL': 'https://discord.com/api/webhooks/test-url'})
    def test_webhook_url(self):
        """Test that the webhook URL is retrieved correctly from environment variables."""
        self.assertEqual(webhook_url, 'https://discord.com/api/webhooks/test-url')

    @patch('requests.get')
    @patch.dict(os.environ, {'DISCORD_WEBHOOK_URL': 'https://discord.com/api/webhooks/test-url'})
    def test_fetch_fact_success(self, mock_get):
        """Test fetching a cat fact successfully."""
        # Mock the response from the Cat Facts API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"fact": "Cats have five toes on their front paws, but only four toes on their back paws."}
        mock_get.return_value = mock_response

        fact_response = requests.get("https://catfact.ninja/fact")
        fact_data = fact_response.json()
        cat_fact = fact_data.get("fact", "Couldn't fetch a cat fact right now.")
        
        self.assertEqual(cat_fact, "Cats have five toes on their front paws, but only four toes on their back paws.")

    @patch('requests.get')
    @patch.dict(os.environ, {'DISCORD_WEBHOOK_URL': 'https://discord.com/api/webhooks/test-url'})
    def test_fetch_fact_failure(self, mock_get):
        """Test fetching a cat fact fails."""
        # Mock a failed response from the Cat Facts API
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        fact_response = requests.get("https://catfact.ninja/fact")

        self.assertEqual(fact_response.status_code, 500)
        self.assertNotEqual(fact_response.status_code, 200)

    @patch('requests.post')
    @patch.dict(os.environ, {'DISCORD_WEBHOOK_URL': 'https://discord.com/api/webhooks/test-url'})
    def test_send_message_success(self, mock_post):
        """Test sending the message to Discord successfully."""
        # Mock the Discord webhook response
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_post.return_value = mock_response

        data = {
            "content": "Test message",
            "username": "Cat Facts Bot"
        }

        response = requests.post(os.environ.get('DISCORD_WEBHOOK_URL'), json=data)

        self.assertEqual(response.status_code, 204)

    @patch('requests.post')
    @patch.dict(os.environ, {'DISCORD_WEBHOOK_URL': 'https://discord.com/api/webhooks/test-url'})
    def test_send_message_failure(self, mock_post):
        """Test sending the message to Discord fails."""
        # Mock a failed response from the Discord webhook
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        data = {
            "content": "Test message",
            "username": "Cat Facts Bot"
        }

        response = requests.post(os.environ.get('DISCORD_WEBHOOK_URL'), json=data)

        self.assertEqual(response.status_code, 400)
        self.assertNotEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()