import pandas as pd

from task_analyzer import settings
from task_analyzer.clients import jira
from task_analyzer.services import actions

jira_client = jira.JiraClient()

for status in jira_client.get_statuses():
    actions.create_or_update_status(
        external_id=status.get('id'),
        datasource=status.get('datasource'),
        name=status.get('name'),
    )

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
        assignee_id = None
        if (issue.get('fields') or {}).get('assignee'):
            assignee_id = issue.get('fields').get('assignee').get('accountId')

        # TODO: support multiple sprints
        sprint = None
        if issue.get('fields'):
            jira_sprint = issue.get('fields').get(settings.JIRA_SPRINT_FIELD_ID)[0] \
                if (issue.get('fields').get(settings.JIRA_SPRINT_FIELD_ID) and
                    len(issue.get('fields').get(settings.JIRA_SPRINT_FIELD_ID))) \
                else None

            if jira_sprint:
                sprint = {
                    'datasource': 'JIRA',
                    'starts_at': pd.to_datetime(jira_sprint.get('startDate')),
                    'ends_at': pd.to_datetime(jira_sprint.get('endDate')),
                    'name': jira_sprint.get('name'),
                    'external_id': f"{jira_sprint.get('id')}_"
                                   f"{jira_sprint.get('boardId')}",
                }

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
            labels=(issue.get('fields') or {}).get('labels') or [],
            story_points=(issue.get('fields') or {}).get(settings.JIRA_STORY_POINT_FIELD_ID),
            sprint=sprint,
        )
