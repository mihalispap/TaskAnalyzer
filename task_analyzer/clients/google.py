from typing import Optional

import requests

from task_analyzer import settings


class GoogleClient:
    _datasource: str = "GOOGLE"

    def __init__(self, space_id: Optional[str] = None, webhook_id: Optional[str] = None):
        self._headers = {"Accept": "application/json"}
        self._webhook_url = (f"https://chat.googleapis.com/v1/spaces/"
                             f"{space_id if space_id else settings.GOOGLE_CHAT_SPACE_ID}/messages?"
                             f"key={webhook_id if webhook_id else settings.GOOGLE_CHAT_WEBHOOK_ID}")

    def send_message(
            self,
            content: str,
            requested_user_id: Optional[str] = None,
            tagged_user_id: Optional[str] = None,
    ):
        tagged = f"{content}!"
        if requested_user_id and tagged_user_id:
            tagged = (f"Hey <users/{tagged_user_id}>, <users/{requested_user_id}> wants to ask you about: {content}."
                      f"Do you have any questions? You can always ask them at the upcoming buffer :)")
        elif requested_user_id:
            tagged = f"Hey <users/{requested_user_id}>, {content}."
        elif tagged_user_id:
            tagged = f"Hey <users/{tagged_user_id}>, {content}."

        message = {
            "text": f"{tagged}"
        }
        requests.post(self._webhook_url, headers=self._headers, json=message)
