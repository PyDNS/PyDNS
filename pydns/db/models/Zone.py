from sqlalchemy import Column, Integer, String, Boolean
from . import Model


class Zone(Model):
    # id is the uuid of the record
    id = Column(String(36), primary_key=True, unique=True)
    domain = Column(String(255), unique=True)
    active = Column(Boolean(True))
