import os

from dotenv import load_dotenv

load_dotenv()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Database
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DATABASE_URL = os.getenv("DATABASE_URL", None)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Jira
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

JIRA_API_TOKEN = os.getenv("API_TOKEN", None)
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN", None)
JIRA_EMAIL = os.getenv("JIRA_EMAIL", None)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Metabase
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

METABASE_DOMAIN = os.getenv("METABASE_DOMAIN", None)
METABASE_USERNAME = os.getenv("METABASE_USERNAME", None)
METABASE_PASSWORD = os.getenv("METABASE_PASSWORD", None)
