import pandas as pd

from task_analyzer import settings
from task_analyzer.clients import google
from task_analyzer.services import actions

google_client = google.GoogleClient()
google_client.send_message(
    content="{TEXT_MESSAGE}",
    requested_user_id="{RID}",
)