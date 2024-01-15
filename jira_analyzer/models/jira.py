from sqlalchemy import String
from sqlalchemy import orm

from jira_analyzer.shared import model


class JiraBase(model.Base):
    name: orm.Mapped[str] = orm.mapped_column(String(256))
    jira_id: orm.Mapped[str] = orm.mapped_column(String(256))

    __id_constituents__ = ["jira_id"]


class Project(JiraBase):
    __tablename__ = "project"
    __id_prefix__ = "prj-"
