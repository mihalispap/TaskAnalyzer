import datetime
from typing import Optional

from jira_analyzer.models import jira

from jira_analyzer import db
from jira_analyzer.repos import repos


def create_or_update_project(
        external_id: str,
        datasource: str,
        name: str,
) -> jira.Project:
    is_new = False
    with db.session_scope() as session:
        repo = repos.ProjectRepo(session)
        entity = repo.get_by_external_id_and_datasource(
            external_id=external_id,
            datasource=datasource,
        )
        if not entity:
            entity = jira.Project(
                name=name,
                external_id=external_id,
                datasource=datasource,
            )
            is_new = True
        entity.name = name
        entity.external_id = external_id
        entity.datasource = datasource

        if is_new:
            entity = repo.save(entity)

    return entity


def create_or_update_assignee(
        external_id: str,
        datasource: str,
        name: str,
) -> jira.Project:
    is_new = False
    with db.session_scope() as session:
        repo = repos.AssigneeRepo(session)
        entity = repo.get_by_external_id_and_datasource(
            external_id=external_id,
            datasource=datasource,
        )
        if not entity:
            entity = jira.Assignee(
                name=name,
                external_id=external_id,
                datasource=datasource,
            )
            is_new = True
        entity.name = name
        entity.external_id = external_id
        entity.datasource = datasource

        if is_new:
            entity = repo.save(entity)

    return entity


def create_or_update_task(
        external_id: str,
        datasource: str,
        name: str,
        created_at: datetime.datetime,
        updated_at: datetime.datetime,
        status: str,
        project_external_id: str,
        assignee_external_id: Optional[str] = None,
) -> jira.Task:
    is_new = False
    with db.session_scope() as session:
        project_repo = repos.ProjectRepo(session)
        project = project_repo.get_by_external_id_and_datasource(
            external_id=project_external_id,
            datasource=datasource,
        )
        if not project:
            raise ValueError(f"Project: {project_external_id} of {datasource} not found")

        assignee = None
        assignee_repo = repos.AssigneeRepo(session)
        if assignee_external_id:
            assignee = assignee_repo.get_by_external_id_and_datasource(
                external_id=assignee_external_id,
                datasource=datasource,
            )

        repo = repos.TaskRepo(session)
        entity = repo.get_by_external_id_and_datasource(
            external_id=external_id,
            datasource=datasource,
        )
        if not entity:
            entity = jira.Task(
                name=name,
                external_id=external_id,
                datasource=datasource,
            )
            is_new = True
        entity.name = name
        entity.external_id = external_id
        entity.datasource = datasource
        entity.created_at = created_at
        entity.updated_at = updated_at
        entity.task_status = status
        entity.project_id = project.id
        entity.assignee_id = assignee.id if assignee else None

        if is_new:
            entity = repo.save(entity)

    return entity
