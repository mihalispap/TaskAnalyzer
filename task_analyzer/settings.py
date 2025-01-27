import os

from dotenv import load_dotenv

load_dotenv()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Database
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DATABASE_URL = os.getenv("DATABASE_URL", None)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Internal Settings
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SLUG_GENERATION_RETRIES = int(os.getenv("SLUG_GENERATION_RETRIES", 5))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Jira
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

JIRA_API_TOKEN = os.getenv("API_TOKEN", None)
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN", None)
JIRA_EMAIL = os.getenv("JIRA_EMAIL", None)
JIRA_EXTERNAL_DEPENDENCY_FIELD_ID = os.getenv("JIRA_EXTERNAL_DEPENDENCY_FIELD_ID", None)
JIRA_STORY_POINT_FIELD_ID = os.getenv("JIRA_STORY_POINT_FIELD_ID", None)
JIRA_SPRINT_FIELD_ID = os.getenv("JIRA_SPRINT_FIELD_ID", None)
JIRA_TARGET_STATUS_ID = os.getenv("JIRA_TARGET_STATUS_ID", None)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Metabase
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

METABASE_DOMAIN = os.getenv("METABASE_DOMAIN", None)
METABASE_USERNAME = os.getenv("METABASE_USERNAME", None)
METABASE_PASSWORD = os.getenv("METABASE_PASSWORD", None)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Google Chat
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GOOGLE_CHAT_SPACE_ID = os.getenv("GOOGLE_CHAT_SPACE_ID", None)
GOOGLE_CHAT_WEBHOOK_ID = os.getenv("GOOGLE_CHAT_WEBHOOK_ID", None)
