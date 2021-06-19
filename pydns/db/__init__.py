class Backend:

    def __init__(self):
        self.connected = False
        self.connection = None

    def connect(self):
        pass

    def close(self):
        pass

    def isConnected(self):
        return self.connected

    def createTables(self):
        pass

    def commit(self):
        pass

    def query(self, sql):
        pass
