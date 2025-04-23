import os

from dotenv import load_dotenv
from fastapi_mail import MessageSchema, MessageType, FastMail, ConnectionConfig

load_dotenv()
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_USERNAME,
    MAIL_PORT=587,  # or 465 for SSL
    MAIL_SERVER="smtp.gmail.com",  # e.g., Gmail
    MAIL_STARTTLS=True,  # TLS mode
    MAIL_SSL_TLS=False,  # or True if using SSL (port 465)
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)
async def send_remedy_email(to: str, pdf_path: str):
    with open(pdf_path, "rb") as f:
        file_data = f.read()

    message = MessageSchema(
        subject="Your Remedy PDF from HomeCure Kids",
        recipients=[to],  # list of emails
        body="Hello! Please find your remedy PDF attached.",
        attachments=[str(pdf_path)
                     ],
        subtype=MessageType.plain
    )

    fm = FastMail(conf)
    await fm.send_message(message)

