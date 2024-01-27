from typing import List, Dict, Optional

import requests
import json

from requests import auth
from jira_analyzer import settings


class JiraClient:
    _datasource: str = "JIRA"

    def __init__(self):
        self._headers = {"Accept": "application/json"}
        self._base_endpoint = f"https://{settings.JIRA_DOMAIN}.atlassian.net/rest/api/3"

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

            projects.extend([{
                "datasource": self._datasource,
                **val
            } for val in response.get("values") or []])
            if response.get("isLast"):
                break

        return projects

    def get_issues(self, project_id: Optional[str]) -> List[Dict]:
        # TODO: add optional param to fetch issues after a creation date

        offset = 0
        issues = []

        while True:
            url = f"{self._base_endpoint}/search?maxResults=1000&startAt={offset}"
            if project_id:
                url += f"&jql=project={project_id}"
            response = requests.get(
                url,
                headers=self._headers,
                auth=self._authenticate,
            ).json()
            offset += len(response.get("issues"))

            issues.extend([{
                "datasource": self._datasource,
                **val
            } for val in response.get("issues") or []])
            if not len(response.get("issues")):
                break

        return issues
