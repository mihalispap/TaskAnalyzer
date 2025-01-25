import pandas as pd

from task_analyzer import settings
from task_analyzer.clients import jira
from task_analyzer.services import actions

jira_client = jira.JiraClient()
for user in jira_client.get_users():
    actions.create_or_update_user(
        external_id=user.get('accountId'),
        datasource=user.get('datasource'),
        name=user.get('displayName'),
        email=user.get('emailAddress'),
    )

for project in jira_client.get_projects():
    actions.create_or_update_project(
        external_id=project.get('id'),
        datasource=project.get('datasource'),
        name=project.get('name'),
    )

    for issue in jira_client.get_issues(project_id=project.get('id')):
        if not 'call/progress' in issue.get('fields').get('summary'):
            continue

        assignee_id = None
        if (issue.get('fields') or {}).get('assignee'):
            assignee_id = issue.get('fields').get('assignee').get('accountId')

        actions.create_or_update_task(
            external_id=issue.get('id'),
            datasource=issue.get('datasource'),
            name=(issue.get('fields') or {}).get('summary'),
            created_at=pd.to_datetime((issue.get('fields') or {}).get('created')),
            updated_at=pd.to_datetime((issue.get('fields') or {}).get('updated')),
            status=(issue.get('fields') or {}).get('status').get('name'),
            project_external_id=(issue.get('fields') or {}).get('project').get('id'),
            assignee_external_id=assignee_id,
            external_dependency_email=(issue.get('fields') or {}).get(settings.JIRA_EXTERNAL_DEPENDENCY_FIELD_ID),
        )
