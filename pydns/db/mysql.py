from pydns import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import Backend
from pydns.db.models import Zone
from pydns.db.models.meta import Base


class MySql(Backend):

    def __init__(self):
        super().__init__()
        self.Base = Base

        if config.getString("database", "password") is None:
            self.connectionUri = "mysql://%s@%s:%d/%s" % (
                config.getString("database", "username"),
                config.getString("database", "host"),
                config.getInt("database", "port"),
                config.getString("database", "database")
            )
        else:
            self.connectionUri = "mysql://%s:%s@%s:%d/%s" % (
                config.getString("database", "username"),
                config.getString("database", "password"),
                config.getString("database", "host"),
                config.getInt("database", "port"),
                config.getString("database", "database")
            )

        # initialize the engine
        self.db = create_engine(self.connectionUri)

        # create the session
        session = sessionmaker(bind=self.db)
        self.session = session()

    def connect(self):
        self.connection = self.db.connect()
        self.connected = True

    def close(self):
        self.connection.close()
        self.connection = None
        self.connected = False

    def createTables(self):
        self.Base.metadata.create_all(self.db)

    def query(self, sql):
        # make sure we are connected
        if not self.isConnected():
            self.connect()

        result = self.db.execute(sql)
        if result:
            return result
        else:
            return None

    def commit(self):
        self.session.commit()

    def getZone(self, domain):
        zone = self.session.query(Zone).filter_by(domain=domain).first()
        if zone is not None:
            print(zone)