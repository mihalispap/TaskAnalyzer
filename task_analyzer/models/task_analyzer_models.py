import datetime
from typing import List

from sqlalchemy import orm, ForeignKey, String, DateTime
from task_analyzer.shared import model


class Project(model.ModelBase):
    __tablename__ = "project"
    __id_prefix__ = "prj-"

    tasks: orm.Mapped[List["Task"]] = orm.relationship(back_populates="project")


class Task(model.ModelBase):
    __tablename__ = "task"
    __id_prefix__ = "tsk-"

    project_id: orm.Mapped[str] = orm.mapped_column(ForeignKey("project.id"))
    project: orm.Mapped["Project"] = orm.relationship(back_populates="tasks")

    task_status: orm.Mapped[str] = orm.mapped_column(String(64), nullable=True)

    created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(DateTime)
    updated_at: orm.Mapped[datetime.datetime] = orm.mapped_column(DateTime, nullable=True)

    assignee_id: orm.Mapped[str] = orm.mapped_column(ForeignKey("assignee.id"), nullable=True)
    assignee: orm.Mapped["Assignee"] = orm.relationship(back_populates="tasks")


class Assignee(model.ModelBase):
    __tablename__ = "assignee"
    __id_prefix__ = "asg-"

    tasks: orm.Mapped[List["Task"]] = orm.relationship(back_populates="assignee")
