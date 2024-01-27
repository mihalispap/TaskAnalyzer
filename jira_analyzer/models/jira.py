from jira_analyzer.shared import model


class Project(model.ModelBase):
    __tablename__ = "project"
    __id_prefix__ = "prj-"
