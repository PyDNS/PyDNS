from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import declarative_base
import inflect


class Base(object):

    @declared_attr
    def __tablename__(cls):
        pluralizer = inflect.engine()
        return pluralizer.plural(cls.__name__.lower())


Base = declarative_base(cls=Base)
