import datetime
from typing import Optional, Iterator, List

from sqlalchemy import desc, and_

from task_analyzer.models import task_analyzer_models
from task_analyzer.shared import repos


class ProjectRepo(repos.BaseRepo[task_analyzer_models.Project]):
    """Query repository for Projects."""
    _type = task_analyzer_models.Project

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
