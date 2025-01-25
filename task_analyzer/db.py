from typing import Optional

from task_analyzer import settings
from sqlalchemy import orm
from sqlalchemy import create_engine

from contextlib import contextmanager

# Database Session/Conf
_session = None
_using_existent = False
_db_url: str = settings.DATABASE_URL


# TODO: switch to a cls
@contextmanager
def session_scope(session: Optional[orm.sessionmaker] = None):
    """Provide a transactional scope around a series of operations."""
    global _session
    global _using_existent

    if session:
        _session = session
        _using_existent = True

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
        if not _using_existent:
            _session.close()
