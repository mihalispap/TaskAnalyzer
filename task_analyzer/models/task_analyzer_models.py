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

    assignee_id: orm.Mapped[str] = orm.mapped_column(ForeignKey("user.id"), nullable=True)
    assignee: orm.Mapped["User"] = orm.relationship(foreign_keys=[assignee_id])

    external_dependency_id: orm.Mapped[str] = orm.mapped_column(ForeignKey("user.id"), nullable=True)
    external_dependency: orm.Mapped["User"] = orm.relationship(
        foreign_keys=[external_dependency_id],
    )


class User(model.ModelBase):
    __tablename__ = "user"
    __id_prefix__ = "usr-"

    email: orm.Mapped[str] = orm.mapped_column(String(256), nullable=True)
