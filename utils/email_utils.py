import aiosmtplib
from email.message import EmailMessage
import os

async def send_verification_email(to_email: str, fullname: str, token: str):
    msg = EmailMessage()
    msg["From"] = os.getenv("EMAIL_FROM")
    msg["To"] = to_email
    msg["Subject"] = "Please verify your email"

    verification_link = f"{os.getenv('FRONTEND_URL')}/user/verify-email?token={token}"
    msg.set_content(f"Hi {fullname}, please verify your email by clicking the following link: {verification_link}")

    await aiosmtplib.send(
        msg,
        hostname=os.getenv("EMAIL_HOST"),
        port=465,  # Sử dụng port 465 cho SSL
        ssl=True,   # Sử dụng SSL thay vì STARTTLS
        username=os.getenv("EMAIL_FROM"),
        password=os.getenv("EMAIL_PASSWORD"),
    )
