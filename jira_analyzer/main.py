from jira_analyzer.clients import jira

jira_client = jira.JiraClient()
jira_client.get_projects()
