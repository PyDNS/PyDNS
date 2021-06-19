from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from .meta import Base


class Zone(Base):
    # id is the uuid of the zone
    id = Column(String(36), primary_key=True, unique=True)
    domain = Column(String(255), unique=True)
    active = Column(Boolean(True))

    records = relationship("Record", lazy="dynamic")
