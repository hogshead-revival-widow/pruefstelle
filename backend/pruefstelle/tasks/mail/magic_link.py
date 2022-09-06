from pydantic import EmailStr
from .send import send

from ...config import settings


def send_magic_link(to: EmailStr, token: str):
    to = EmailStr(to)
    subject = "Dein Anmelde-Link"
    link = f"{settings.frontend.base_url}/auth?link={token}"
    content = f"""\
        <p>Klicke <a href="{link}">hier</a>, um dich anzumelden.</p>
        <br/>
        <p>Oder kopiere alternativ diesen Link in deinen Browser: <pre>{link}</pre></p>
        """
    send(to, subject=subject, content=content, as_html=True)
