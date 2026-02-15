import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import logging
from app.config import get_settings
from app.schemas import EmailSchema

settings = get_settings()
logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.ses_client = None
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY and settings.AWS_REGION:
            try:
                self.ses_client = boto3.client(
                    'ses',
                    region_name=settings.AWS_REGION,
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                )
            except Exception as e:
                logger.error(f"Failed to initialize AWS SES client: {e}")
        else:
            logger.warning("AWS SES credentials missing. Email service will run in mock mode.")

    def send_email(self, email_data: EmailSchema):
        if not self.ses_client:
            logger.info(f"Mocking email send to {email_data.to_email}: {email_data.subject}")
            return {"status": "mocked", "data": email_data.model_dump()}

        msg = MIMEMultipart()
        msg['Subject'] = email_data.subject
        msg['From'] = "noreply@tcgplatform.com" 
        msg['To'] = email_data.to_email

        body = MIMEText(email_data.body, 'plain')
        msg.attach(body)

        if email_data.attachment_path and os.path.exists(email_data.attachment_path):
            with open(email_data.attachment_path, 'rb') as f:
                part = MIMEApplication(f.read())
                part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(email_data.attachment_path))
                msg.attach(part)

        try:
            response = self.ses_client.send_raw_email(
                Source=msg['From'],
                Destinations=[email_data.to_email],
                RawMessage={'Data': msg.as_string()}
            )
            logger.info(f"Email sent to {email_data.to_email}: ID {response.get('MessageId')}")
            return response
        except ClientError as e:
            logger.error(f"Failed to send email to {email_data.to_email}: {e}")
            return {"error": str(e)}

email_service = EmailService()
