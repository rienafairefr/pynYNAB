import json
import uuid

from sqlalchemy import String, types
from sqlalchemy import TypeDecorator


class ArrayType(TypeDecorator):
    """ Sqlite-like does not support arrays.
        Let's use a custom type decorator.

        See http://docs.sqlalchemy.org/en/latest/core/types.html#sqlalchemy.types.TypeDecorator
    """
    impl = String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)

    def copy(self, **kw):
        return ArrayType(self.impl.length)


class AmountType(types.TypeDecorator):
    impl = types.Integer

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(types.Integer)

    def process_bind_param(self, value, dialect):
        return int(value * 1000) if value is not None else None

    def process_result_value(self, value, dialect):
        return float(value) / 1000 if value is not None else None
