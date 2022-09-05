from uuid import UUID
from pydantic import EmailStr
from .send import send

from ...config import settings


def send_new_case_email(to: str, case_id: UUID, title: str):
    to = EmailStr(to)
    subject = f"Link: Fall '{title}'"
    content = f"""\
        Hier ist der Link zu deinem neuen Fall:

            http://{settings.frontend.base_url}{settings.frontend.case_path}/{case_id}

        """
    send(to, subject=subject, content=content)
