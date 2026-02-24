from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from backlog_app.config import settings


async def send_email(
    recipient: str,
    subject: str,
    plain_content: str,
    html_content: str = "",
):
    message = MIMEMultipart("alternative")
    message["From"] = settings.smtp.username
    message["To"] = recipient
    message["Subject"] = subject

    plain_text_message = MIMEText(
        plain_content,
        "plain",
        "utf-8",
    )
    message.attach(plain_text_message)

    if html_content:
        html_message = MIMEText(
            html_content,
            "html",
            "utf-8",
        )
        message.attach(html_message)

    await aiosmtplib.send(
        message,
        hostname=settings.smtp.server,
        port=settings.smtp.port,
        use_tls=settings.smtp.use_tls,
        username=settings.smtp.username,
        password=settings.smtp.password,
    )
