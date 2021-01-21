from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .meta import Model


class Record(Model):
    # id is the uuid of the record
    id = Column(String(36), primary_key=True, unique=True)
    zone_id = Column(String(36), ForeignKey("zones.id"))
    type = Column(String(50))

    zone = relationship("Zone", lazy="joined")
