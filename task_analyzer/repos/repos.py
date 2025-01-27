from typing import Optional, List

from sqlalchemy import and_

from task_analyzer.models import task_analyzer_models
from task_analyzer.shared import repos


class SprintRepo(repos.BaseRepo[task_analyzer_models.Sprint]):
    """Query repository for Sprints."""
    _type = task_analyzer_models.Sprint


class LabelRepo(repos.BaseRepo[task_analyzer_models.Label]):
    """Query repository for Labels."""
    _type = task_analyzer_models.Label


class StatusRepo(repos.BaseRepo[task_analyzer_models.Status]):
    """Query repository for Statuses."""
    _type = task_analyzer_models.Status


class ProjectRepo(repos.BaseRepo[task_analyzer_models.Project]):
    """Query repository for Projects."""
    _type = task_analyzer_models.Project

    # TODO: remove
    def get_by_external_id_and_datasource(
            self,
            external_id: str,
            datasource: str,
    ) -> Optional[task_analyzer_models.Project]:
        """Get an object on its id constituents"""
        filters = [
            task_analyzer_models.Project.external_id == external_id,
            task_analyzer_models.Project.datasource == datasource,
        ]
        return self.session.query(task_analyzer_models.Project).filter(
            and_(*filters)
        ).one_or_none()


class TaskRepo(repos.BaseRepo[task_analyzer_models.Task]):
    """Query repository for Tasks."""
    _type = task_analyzer_models.Task

    def get_by_status_and_existent_dependency(self, status: str) -> List[task_analyzer_models.Task]:
        """Get an object on its status having a dependency"""
        filters = [
            task_analyzer_models.Task.task_status == status,
            task_analyzer_models.Task.external_dependency_id != None,
        ]
        return self.session.query(task_analyzer_models.Task).filter(
            and_(*filters)
        ).all()

    # TODO: remove
    def get_by_external_id_and_datasource(
            self,
            external_id: str,
            datasource: str,
    ) -> Optional[task_analyzer_models.Task]:
        """Get an object on its id constituents"""
        filters = [
            task_analyzer_models.Task.external_id == external_id,
            task_analyzer_models.Task.datasource == datasource,
        ]
        return self.session.query(task_analyzer_models.Task).filter(
            and_(*filters)
        ).one_or_none()


class UserRepo(repos.BaseRepo[task_analyzer_models.User]):
    """Query repository for Users."""
    _type = task_analyzer_models.User

    # TODO: remove
    def get_by_external_id_and_datasource(
            self,
            external_id: str,
            datasource: str,
    ) -> Optional[task_analyzer_models.User]:
        """Get an object on its id constituents"""
        filters = [
            task_analyzer_models.User.external_id == external_id,
            task_analyzer_models.User.datasource == datasource,
        ]
        return self.session.query(task_analyzer_models.User).filter(
            and_(*filters)
        ).one_or_none()

    def get_by_email(
            self,
            email: str,
    ) -> Optional[task_analyzer_models.User]:
        """Get an object on its email"""
        filters = [
            task_analyzer_models.User.email == email,
        ]
        return self.session.query(task_analyzer_models.User).filter(
            and_(*filters)
        ).one_or_none()
