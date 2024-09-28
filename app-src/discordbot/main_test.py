import unittest
from unittest.mock import patch, MagicMock
import os
import requests

# Import the script that contains the logic (assuming it's named main.py)
import main


class TestSendMessage(unittest.TestCase):

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_webhook_url(self):
        """Test when the DISCORD_WEBHOOK_URL environment variable is missing."""
        with patch('builtins.print') as mocked_print, self.assertRaises(SystemExit):
            # Re-run the import to execute the code with a cleared environment
            main

            # Verify that the error message is printed
            mocked_print.assert_called_once_with("Error: Webhook URL is not set in the environment variables.")

    @patch.dict(os.environ, {'DISCORD_WEBHOOK_URL': 'https://discord.com/api/webhooks/test-url'})
    @patch('requests.post')
    def test_successful_message_send(self, mock_post):
        """Test when the message is sent successfully."""
        # Mock response object to mimic a successful POST request
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_post.return_value = mock_response

        with patch('builtins.print') as mocked_print:
            # Re-run the import to execute the code with the webhook set
            main

            # Verify that the success message is printed
            mocked_print.assert_called_once_with("Message sent successfully!")

    @patch.dict(os.environ, {'DISCORD_WEBHOOK_URL': 'https://discord.com/api/webhooks/test-url'})
    @patch('requests.post')
    def test_failed_message_send(self, mock_post):
        """Test when the message fails to send due to a bad response status code."""
        # Mock response object to mimic a failed POST request
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        with patch('builtins.print') as mocked_print:
            # Re-run the import to execute the code with the webhook set
            main

            # Verify that the error message is printed with the correct status code
            mocked_print.assert_called_once_with("Failed to send message. Status code: 400")


if __name__ == '__main__':
    unittest.main()
