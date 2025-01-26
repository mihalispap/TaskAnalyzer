import pandas as pd

from task_analyzer import settings, db
from task_analyzer.clients import google, jira
from task_analyzer.services import actions

google_client = google.GoogleClient()
jira_client = jira.JiraClient()

with db.session_scope() as session:
    for issue in actions.find_issues_by_status_and_existent_dependency(status="To Do", _session=session):
        google_client.send_message(
            content=issue.name,
            requested_user_id=issue.assignee.gid,
            tagged_user_id=issue.external_dependency.gid,
        )
        jira_client.update_issue_status(
            issue_jira_id=issue.external_id,
            status_jira_id=settings.JIRA_TARGET_STATUS_ID,
        )
