import datetime
from typing import Optional, Iterator, List

from sqlalchemy import desc, and_

from jira_analyzer.models import jira
from jira_analyzer.shared import repos


class ProjectRepo(repos.BaseRepo[jira.Project]):
    """Query repository for Projects."""

    def get_by_external_id_and_datasource(
            self,
            external_id: str,
            datasource: str,
    ) -> Optional[jira.Project]:
        """Get an object on its id constituents"""
        filters = [
            jira.Project.external_id == external_id,
            jira.Project.datasource == datasource,
        ]
        return self.session.query(jira.Project).filter(
            and_(*filters)
        ).one_or_none()


class TaskRepo(repos.BaseRepo[jira.Task]):
    """Query repository for Tasks."""

    def get_by_external_id_and_datasource(
            self,
            external_id: str,
            datasource: str,
    ) -> Optional[jira.Task]:
        """Get an object on its id constituents"""
        filters = [
            jira.Task.external_id == external_id,
            jira.Task.datasource == datasource,
        ]
        return self.session.query(jira.Task).filter(
            and_(*filters)
        ).one_or_none()
