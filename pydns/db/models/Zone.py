from sqlalchemy import Column, Integer, String, Boolean
from . import Model


class Zone(Model):
    id = Column(Integer, primary_key=True)
    domain = Column(String(255))
    active = Column(Boolean(True))
