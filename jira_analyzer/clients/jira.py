from typing import List, Dict

import requests
import json

from requests import auth
from jira_analyzer import settings


class JiraClient:

    def __init__(self):
        self._headers = {"Accept": "application/json"}
        self._base_endpoint = f"https://{settings.JIRA_DOMAIN}.atlassian.net/rest/api/2"

    @property
    def _authenticate(self) -> auth.HTTPBasicAuth:
        return auth.HTTPBasicAuth(settings.JIRA_EMAIL, settings.JIRA_API_TOKEN)

    def get_projects(self) -> List[Dict]:
        offset = 0
        projects = []

        while True:
            url = f"{self._base_endpoint}/project/search?startAt={offset}"
            response = requests.get(
                url,
                headers=self._headers,
                auth=self._authenticate,
            ).json()
            offset += len(response.get("values"))

            projects.extend(response.get("values"))
            if response.get("isLast"):
                break

        return projects
