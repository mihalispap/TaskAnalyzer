from jira_analyzer import settings
from sqlalchemy import orm
from sqlalchemy import create_engine

from contextlib import contextmanager

# Database Session/Conf
_session = None
_db_url: str = settings.DATABASE_URL


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    global _session

    if not _session:
        engine = create_engine(_db_url)
        _session = orm.sessionmaker(engine)()

    try:
        yield _session
        _session.commit()
    except:
        _session.rollback()
        raise
    finally:
        _session.close()
