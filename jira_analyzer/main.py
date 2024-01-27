import pandas as pd

from jira_analyzer.clients import jira
from jira_analyzer.services import actions

jira_client = jira.JiraClient()
for project in jira_client.get_projects():
    actions.create_or_update_project(
        external_id=project.get('id'),
        datasource=project.get('datasource'),
        name=project.get('name'),
    )

    for issue in jira_client.get_issues(project_id=project.get('id')):
        actions.create_or_update_task(
            external_id=issue.get('id'),
            datasource=issue.get('datasource'),
            name=(issue.get('fields') or {}).get('summary'),
            created_at=pd.to_datetime((issue.get('fields') or {}).get('created')),
            updated_at=pd.to_datetime((issue.get('fields') or {}).get('updated')),
            status=(issue.get('fields') or {}).get('status').get('name'),
            project_external_id=(issue.get('fields') or {}).get('project').get('id'),
        )

