from pydns import config
from sqlalchemy import create_engine
from . import Backend
from pydns.db.models import Zone

class MySql(Backend):

    def __init__(self):
        super().__init__()

        self.connectionUri = "mysql://%s:%s@%s:%d/%s" % (
            config.getString("database", "username"),
            config.getString("database", "password"),
            config.getString("database", "host"),
            config.getInt("database", "port"),
            config.getString("database", "database")
        )

        self.db = create_engine(self.connectionUri)

    def connect(self):
        self.connection = self.db.connect()
        self.connected = True

    def close(self):
        self.connection.close()
        self.connection = None
        self.connected = False

    def query(self, sql):
        # make sure we are connected
        if not self.isConnected():
            self.connect()

        result = self.db.execute(sql)
        if result:
            return result
        else:
            return None

    def getZone(self, domain):
        zone = Zone(domain=)
        if results is not None:
            print(results)