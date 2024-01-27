from jira_analyzer.clients import jira
from jira_analyzer.services import actions

jira_client = jira.JiraClient()
for project in jira_client.get_projects():
    actions.create_or_update_project(
        external_id=project.get('id'),
        datasource='JIRA',
        name=project.get('name'),
    )
