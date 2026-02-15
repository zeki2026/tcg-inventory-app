import pytest
from unittest.mock import MagicMock, patch
from app.services.email_service import EmailService
from app.services.telegram_service import TelegramService
from app.schemas import EmailSchema, TelegramSchema

@pytest.fixture
def mock_ses_client():
    with patch("boto3.client") as mock_boto:
        yield mock_boto.return_value

@pytest.fixture
def mock_telegram_bot():
    with patch("telegram.Bot") as mock_bot:
        yield mock_bot.return_value

def test_email_service_mocked(mock_ses_client):
    # Test sending email when SES is configured (mocked)
    with patch("app.services.email_service.settings") as mock_settings:
        mock_settings.AWS_ACCESS_KEY_ID = "test"
        mock_settings.AWS_SECRET_ACCESS_KEY = "test"
        mock_settings.AWS_REGION = "us-east-1"
        
        service = EmailService()
        # Force set client because __init__ might run before patch takes full effect in some envs
        service.ses_client = mock_ses_client

        payload = EmailSchema(
            to_email="test@example.com",
            subject="Test",
            body="Hello"
        )
        service.send_email(payload)
        
        mock_ses_client.send_raw_email.assert_called_once()

@pytest.mark.asyncio
async def test_telegram_service_mocked():
    # Test sending telegram message
    with patch("app.services.telegram_service.settings") as mock_settings:
        mock_settings.TELEGRAM_BOT_TOKEN = "test_token"
        mock_settings.TELEGRAM_CHAT_ID = "123456"
        
        with patch("app.services.telegram_service.Bot") as MockBot:
            mock_bot_instance = MockBot.return_value
            # Async mock
            mock_bot_instance.send_message = MagicMock()
            async def async_send(*args, **kwargs):
                return True
            mock_bot_instance.send_message.side_effect = async_send

            service = TelegramService()
            service.bot = mock_bot_instance
            service.chat_id = "123456"

            payload = TelegramSchema(message="Test Message")
            await service.send_message(payload)
            
            mock_bot_instance.send_message.assert_called_once_with(chat_id="123456", text="Test Message")
