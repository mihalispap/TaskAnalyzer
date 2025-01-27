import datetime
from typing import List

from sqlalchemy import orm, ForeignKey, String, DateTime, Table, Column, Float
from task_analyzer.shared import model

task_labels = Table('task_labels', model.ModelBase.metadata,
                    Column('task_id', ForeignKey('task.id', ondelete="CASCADE"), index=True),
                    Column('label_id', ForeignKey('label.id', ondelete="CASCADE"), index=True)
                    )


class Label(model.ModelBase):
    __tablename__ = "label"
    __id_prefix__ = "lbl-"


class Status(model.ModelBase):
    __tablename__ = "status"
    __id_prefix__ = "stt-"

    name: orm.Mapped[str] = orm.mapped_column(String(128))


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
    story_points: orm.Mapped[float] = orm.mapped_column(Float, nullable=True)

    created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(DateTime)
    updated_at: orm.Mapped[datetime.datetime] = orm.mapped_column(DateTime, nullable=True)

    assignee_id: orm.Mapped[str] = orm.mapped_column(ForeignKey("user.id"), nullable=True)
    assignee: orm.Mapped["User"] = orm.relationship(foreign_keys=[assignee_id])

    external_dependency_id: orm.Mapped[str] = orm.mapped_column(ForeignKey("user.id"), nullable=True)
    external_dependency: orm.Mapped["User"] = orm.relationship(
        foreign_keys=[external_dependency_id],
    )

    labels = orm.relationship('Label', secondary=task_labels)

    def associate_labels(self, labels: List[Label]):
        self.labels = []
        for label in labels:
            if not any(
                    [
                        l
                        for l in self.labels
                        if l.id == label.id
                    ]
            ):
                self.labels.append(label)


class User(model.ModelBase):
    __tablename__ = "user"
    __id_prefix__ = "usr-"

    email: orm.Mapped[str] = orm.mapped_column(String(256), nullable=True)
    gid: orm.Mapped[str] = orm.mapped_column(String(128), nullable=True)
