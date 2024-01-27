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
