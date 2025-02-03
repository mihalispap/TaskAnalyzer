import datetime
from typing import Optional, Union, Type, List, Dict

from unique_names_generator import get_random_name  # type: ignore # noqa
from unique_names_generator.data import ADJECTIVES, ANIMALS, NAMES  # type: ignore # noqa

from task_analyzer.models import task_analyzer_models

from task_analyzer import db, settings
from task_analyzer.repos import repos


def _generate_unique_entity_slug(
        entity: Union[
            Type[task_analyzer_models.User],
            Type[task_analyzer_models.Project],
            Type[task_analyzer_models.Task],
            Type[task_analyzer_models.Status],
            Type[task_analyzer_models.Label],
            Type[task_analyzer_models.Sprint],
        ],
) -> str:
    for _ in range(0, settings.SLUG_GENERATION_RETRIES):
        slug = get_random_name(
            combo=[NAMES, ADJECTIVES, ANIMALS], separator="-", style="lowercase"
        )
        if not get_entity_by_slug(slug, entity):
            return slug
    raise AttributeError(
        f"After {settings.SLUG_GENERATION_RETRIES} retries no unique slug was generated"
    )


def get_entity_by_slug(
        slug: str,
        entity: Union[
            Type[task_analyzer_models.User],
            Type[task_analyzer_models.Project],
            Type[task_analyzer_models.Task],
            Type[task_analyzer_models.Status],
            Type[task_analyzer_models.Label],
            Type[task_analyzer_models.Sprint],
        ],
) -> Optional[Union[task_analyzer_models.User]]:
    """Get an entity by its slug.

    Args:
        slug: Entity slug.
        entity: Type of entity to query on slug.

    Iterator:
        Optional[Union[task_analyzer_models.User]]

    """
    with db.session_scope() as session:
        repo = None
        match entity:
            case task_analyzer_models.User:
                repo = repos.UserRepo(session)
            case task_analyzer_models.Project:
                repo = repos.ProjectRepo(session)
            case task_analyzer_models.Task:
                repo = repos.TaskRepo(session)
            case task_analyzer_models.Status:
                repo = repos.StatusRepo(session)
            case task_analyzer_models.Label:
                repo = repos.LabelRepo(session)
            case task_analyzer_models.Sprint:
                repo = repos.SprintRepo(session)
            case _:
                raise NotImplementedError(f"Slug entity fetch for {type(entity)} not implemented.")
        return repo.get_by_slug(slug)


def create_or_update_sprint(
        datasource: str,
        name: str,
        external_id: str,
        starts_at: Optional[datetime.datetime] = None,
        ends_at: Optional[datetime.datetime] = None,
        _session=None,
) -> task_analyzer_models.Sprint:
    is_new = False
    with db.session_scope(_session) as session:
        repo = repos.SprintRepo(session)

        if not external_id:
            external_id = _generate_unique_entity_slug(task_analyzer_models.Sprint)
        entity = repo.get_by_external_id_and_datasource(
            external_id=external_id,
            datasource=datasource,
        )
        if not entity:
            entity = task_analyzer_models.Sprint(
                name=name,
                external_id=external_id,
                datasource=datasource,
                slug=_generate_unique_entity_slug(task_analyzer_models.Label),
            )
            is_new = True
        entity.name = name
        entity.external_id = external_id
        entity.datasource = datasource
        entity.starts_at = starts_at
        entity.ends_at = ends_at

        if is_new:
            entity = repo.save(entity)

    return entity


def create_or_update_label(
        datasource: str,
        name: str,
        _session=None,
        external_id: Optional[str] = None,
) -> task_analyzer_models.Label:
    is_new = False
    with db.session_scope(_session) as session:
        repo = repos.LabelRepo(session)

        if not external_id:
            external_id = _generate_unique_entity_slug(task_analyzer_models.Label)
        entity = repo.get_by_name_and_datasource(
            name=name,
            datasource=datasource,
        )
        if not entity:
            entity = task_analyzer_models.Label(
                name=name,
                external_id=external_id,
                datasource=datasource,
                slug=_generate_unique_entity_slug(task_analyzer_models.Label),
            )
            is_new = True
        entity.name = name
        entity.external_id = external_id
        entity.datasource = datasource

        if is_new:
            entity = repo.save(entity)

    return entity


def create_or_update_status(
        external_id: str,
        datasource: str,
        name: str,
) -> task_analyzer_models.Status:
    is_new = False
    with db.session_scope() as session:
        repo = repos.StatusRepo(session)
        entity = repo.get_by_external_id_and_datasource(
            external_id=external_id,
            datasource=datasource,
        )
        if not entity:
            entity = task_analyzer_models.Status(
                name=name,
                external_id=external_id,
                datasource=datasource,
                slug=_generate_unique_entity_slug(task_analyzer_models.Status),
            )
            is_new = True
        entity.name = name
        entity.external_id = external_id
        entity.datasource = datasource

        if is_new:
            entity = repo.save(entity)

    return entity


def create_or_update_project(
        external_id: str,
        datasource: str,
        name: str,
) -> task_analyzer_models.Project:
    is_new = False
    with db.session_scope() as session:
        repo = repos.ProjectRepo(session)
        entity = repo.get_by_external_id_and_datasource(
            external_id=external_id,
            datasource=datasource,
        )
        if not entity:
            entity = task_analyzer_models.Project(
                name=name,
                external_id=external_id,
                datasource=datasource,
                slug=_generate_unique_entity_slug(task_analyzer_models.Project),
            )
            is_new = True
        entity.name = name
        entity.external_id = external_id
        entity.datasource = datasource

        if is_new:
            entity = repo.save(entity)

    return entity


def create_or_update_user(
        datasource: str,
        name: str,
        external_id: Optional[str] = None,
        email: Optional[str] = None,
        _session=None,
) -> task_analyzer_models.User:
    is_new = False
    with db.session_scope(_session) as session:
        repo = repos.UserRepo(session)
        if all([external_id, datasource]):
            entity = repo.get_by_external_id_and_datasource(
                external_id=external_id,
                datasource=datasource,
            )
        elif email:
            entity = repo.get_by_email(
                email=email,
            )
        else:
            raise ValueError(f"Provided params for user creation/update not enough.")

        if not external_id:
            external_id = _generate_unique_entity_slug(task_analyzer_models.User)
        if not entity:
            entity = task_analyzer_models.User(
                name=name,
                external_id=external_id,
                datasource=datasource,
                email=email,
                slug=_generate_unique_entity_slug(task_analyzer_models.User)
            )
            is_new = True
        entity.name = name
        entity.external_id = external_id
        entity.datasource = datasource
        entity.email = email

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
        external_dependency_email: Optional[str] = None,
        labels: Optional[List[str]] = None,
        story_points: Optional[float] = None,
        sprint: Optional[Dict] = None,
) -> task_analyzer_models.Task:
    is_new = False
    with db.session_scope() as session:
        project_repo = repos.ProjectRepo(session)
        project = project_repo.get_by_external_id_and_datasource(
            external_id=project_external_id,
            datasource=datasource,
        )
        if not project:
            raise ValueError(f"Project: {project_external_id} of {datasource} not found")
        project_id = project.id

        assignee_id = None
        user_repo = repos.UserRepo(session)
        if assignee_external_id:
            assignee = user_repo.get_by_external_id_and_datasource(
                external_id=assignee_external_id,
                datasource=datasource,
            )
            assignee_id = assignee.id if assignee else None

        external_dependency_id = None
        if external_dependency_email:
            external_dependency = create_or_update_user(
                datasource=datasource,
                name=external_dependency_email,
                email=external_dependency_email,
                _session=session,
            )
            external_dependency_id = external_dependency.id if external_dependency else None

        label_entities = [
            create_or_update_label(
                name=label,
                datasource=datasource,
                _session=session)
            for label in labels
        ]

        sprint_id = None
        if sprint:
            sprint_entity = create_or_update_sprint(
                _session=session,
                **sprint,
            )
            sprint_id = sprint_entity.id

        repo = repos.TaskRepo(session)
        entity = repo.get_by_external_id_and_datasource(
            external_id=external_id,
            datasource=datasource,
        )
        if not entity:
            entity = task_analyzer_models.Task(
                name=name,
                external_id=external_id,
                datasource=datasource,
                slug=_generate_unique_entity_slug(task_analyzer_models.Task),
            )
            is_new = True
        entity.name = name
        entity.external_id = external_id
        entity.datasource = datasource
        entity.created_at = created_at
        entity.updated_at = updated_at
        entity.task_status = status
        entity.project_id = project_id
        entity.sprint_id = sprint_id
        entity.assignee_id = assignee_id if assignee_id else None
        entity.external_dependency_id = external_dependency_id if external_dependency_id else None
        entity.story_points = story_points
        entity.associate_labels(label_entities)

        if is_new:
            entity = repo.save(entity)

    return entity


def find_issues_by_status_and_existent_dependency(
        status: str,
        _session=None,
) -> List[task_analyzer_models.Task]:
    with db.session_scope(_session) as session:
        repo = repos.TaskRepo(session)
        return repo.get_by_status_and_existent_dependency(status=status)


def find_issues_by_status_and_label(
        status: str,
        label: str,
        _session=None,
) -> List[task_analyzer_models.Task]:
    with db.session_scope(_session) as session:
        repo = repos.TaskRepo(session)
        return repo.get_by_status_and_label(status=status, label=label)
