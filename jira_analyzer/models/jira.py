from typing import List

from sqlalchemy import orm, ForeignKey
from jira_analyzer.shared import model


class Project(model.ModelBase):
    __tablename__ = "project"
    __id_prefix__ = "prj-"

    tasks: orm.Mapped[List["Task"]] = orm.relationship(back_populates="project")


class Task(model.ModelBase):
    __tablename__ = "task"
    __id_prefix__ = "tsk-"

    project_id: orm.Mapped[str] = orm.mapped_column(ForeignKey("project.id"))
    project: orm.Mapped["Project"] = orm.relationship(back_populates="tasks")

