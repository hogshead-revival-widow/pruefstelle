import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from pydantic import EmailStr

from ...config import settings


def send(to: EmailStr, subject: str, content: str, as_html=False):
    message = make_message(to, subject=subject, content=content, as_html=as_html)
    return send_mail(to, message)


def make_message(
    to: EmailStr, subject: str, content: str, as_html=False
) -> MIMEMultipart:

    message = MIMEMultipart("alternative")
    message["Subject"] = f"[Prüfstelle] {subject}"
    message["From"] = settings.mail.sender
    message["To"] = to
    body = MIMEText(content, "plain")
    if as_html:
        body = MIMEText(content, "html")
    message.attach(body)

    return message


def send_mail(to: EmailStr, message: MIMEMultipart):
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(
            settings.mail.host, settings.mail.port, context=context
        ) as server:
            server.login(settings.mail.sender, settings.mail.password)
            server.sendmail(settings.mail.sender, to, message.as_string())
    except smtplib.SMTPException as e:
        print(e)
