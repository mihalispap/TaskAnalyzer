from typing import Generic, TypeVar, Optional

from sqlalchemy import and_
from sqlalchemy.orm.session import Session

from task_analyzer.shared import model

T = TypeVar("T", bound=model.Base)


class BaseRepo(Generic[T]):
    """
        Base class for repositories
    """

    def __init__(self, session: Session):
        self.session = session

    def get(self, id_: str) -> Optional[T]:
        """Get an object on its id"""
        return self.session.query(T).get(id_)

    def save(self, instance: T) -> T:
        """Saves an object instance"""
        self.session.add(instance)
        return instance

    def delete(self, instance: T):
        """Deletes an object instance."""
        self.session.delete(instance)
