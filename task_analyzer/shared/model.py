import uuid
import hashlib
import shortuuid

from typing import Optional, List

from sqlalchemy import orm
from sqlalchemy import Column, String

from sqlalchemy.ext.declarative import declared_attr, declarative_base

Base = declarative_base()


class ModelBase(Base):
    """ORM model class, implementing prefixed uuids."""

    __abstract__ = True

    name: orm.Mapped[str] = orm.mapped_column(String(256))
    external_id: orm.Mapped[str] = orm.mapped_column(String(256))
    datasource: orm.Mapped[str] = orm.mapped_column(String(256))
    slug: orm.Mapped[str] = orm.mapped_column(String(256))

    __id_prefix__: Optional[str] = None

    __id_constituents__: List[str] = ["external_id", "datasource", "slug"]

    def __init__(self, *args, **kwargs):
        """Initialize the base model and set its ID (before writing to the database).
        These IDs are UUIDs so we can be confident that we won't have any collisions.

        """
        super().__init__(*args, **kwargs)
        if not self.id:
            # If the id wasn't set in the constructor, compute one by using the attrs
            # in `__id_constituents__` if any.
            parts = [getattr(self, attr) for attr in self.__id_constituents__]
            self.id = self.compute_id(*parts)

    @classmethod
    def compute_id(cls, *parts) -> str:
        """Computes the model id using the given parts. If no parts are given, the id is
        computed based on a UUID.

        Returns:
            str

        """
        cls.ensure_id_prefix()

        if parts:
            m = hashlib.md5()
            m.update(':'.join([str(p) for p in parts]).encode('utf-8'))
            stable_uuid = uuid.UUID(m.hexdigest())
            id_ = shortuuid.encode(stable_uuid)
        else:
            id_ = shortuuid.uuid()

        # 9 characters should give us sufficient uniqueness guarantees while keeping
        # the ids readable.
        id_ = id_[:9]

        # Prefix and produce a shortuuid like the rest of the models.
        return f'{cls.__id_prefix__}-{id_}'

    @classmethod
    def ensure_id_prefix(cls):
        """Checks whether the class has an id prefix.

        Raises:
            AssertionError

        """
        assert cls.__id_prefix__, (
            f'{cls.__name__} needs an id prefix. Add one by defining an __id_prefix__ '
            f'class property.'
        )

    @declared_attr
    def id(cls):
        """Creates the `id` Column. We need this to be a `declared_attr` to have access
        to the class and the id prefix. The id is generated in the class constructor,
        unless specified by the caller.

        Returns:
            Column

        """
        cls.ensure_id_prefix()
        return Column(String(1024), primary_key=True)
