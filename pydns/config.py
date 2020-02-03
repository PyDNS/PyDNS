from configparser import ConfigParser
import os
from pydns import resource

config = None


def load(fileName=None):
    global config

    if not config:
        if fileName:
            config = Config(fileName=fileName)
        else:
            config = Config()
    return config


class Config:

    def __init__(self, fileName="config.ini"):
        self.config = ConfigParser()
        self.fileName = os.path.join(resource.getWriteableResourcePath(), fileName)
        self.config.read(self.fileName)

        if not os.path.isfile(self.fileName):
            self.createDefault()

    def get(self, section, option):
        value = self.config.has_option(section, option) and self.config.get(section, option) or None
        return value

    def set(self, section, option, value):
        if not self.config.has_section(section):
            self.config.add_section(section)

        self.config.set(section, option, value)

        # Save the config file
        self.save()

    def save(self):
        # Save the config file
        f = open(self.fileName, "w")
        self.config.write(f)
        f.close()

    def createDefault(self):
        self.config.add_section("general")
        self.config.set("general", "ip", "127.0.0.1")
        self.config.set("general", "port", "53")

        self.config.add_section("database")
        self.config.set("database", "backend", "mysql")
        self.config.set("database", "host", "localhost")
        self.config.set("database", "port", "3306")
        self.config.set("database", "username", "root")
        self.config.set("database", "password", "")
        self.config.set("database", "database", "pydns")
        self.save()

    def getString(self, section, option):
        return self.get(section, option)

    def getInt(self, section, option):
        return int(self.get(section, option))

    def getBool(self, section, option):
        return bool(self.get(section, option))
