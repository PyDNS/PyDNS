from sqlalchemy.orm import configure_mappers

# import all models here
from .zone import *
from .record import *

# run configure_mappers after defining all of the models to ensure
# all relationships can be setup
configure_mappers()
