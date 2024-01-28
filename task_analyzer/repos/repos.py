import datetime
from typing import Optional, Iterator, List

from sqlalchemy import desc, and_

from task_analyzer.models import task_analyzer_models
from task_analyzer.shared import repos


class ProjectRepo(repos.BaseRepo[task_analyzer_models.Project]):
    """Query repository for Projects."""

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


class AssigneeRepo(repos.BaseRepo[task_analyzer_models.Assignee]):
    """Query repository for Assignees."""

    def get_by_external_id_and_datasource(
            self,
            external_id: str,
            datasource: str,
    ) -> Optional[task_analyzer_models.Assignee]:
        """Get an object on its id constituents"""
        filters = [
            task_analyzer_models.Assignee.external_id == external_id,
            task_analyzer_models.Assignee.datasource == datasource,
        ]
        return self.session.query(task_analyzer_models.Assignee).filter(
            and_(*filters)
        ).one_or_none()
