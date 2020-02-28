import os
from . import resources
import logging
from logging import handlers
import colorlog

LOG_DIR = os.path.join(resources.getWriteableResourcePath(), "logs")
LOG_FILE = os.path.join(LOG_DIR, 'pydns.log')


class Logger(logging.Logger):

    def __init__(self, name=None):
        super().__init__(name)

        # make sure log directory exists
        if not os.path.isdir(LOG_DIR):
            os.mkdir(LOG_DIR)

        log_format = (
            '[%(asctime)s]'
            '[%(name)s]'
            '[%(levelname)s]'
            ' %(message)s'
        )
        colorlog_format = (
            '%(log_color)s'
            f'{log_format}'
        )

        # setup formatter
        formatter = logging.Formatter(log_format)
        formatter.datefmt = '%m/%d/%Y %I:%M:%S'

        consoleFormatter = colorlog.ColoredFormatter(colorlog_format)
        consoleFormatter.datefmt = '%m/%d/%Y %I:%M:%S'

        # define file handler
        fileHandler = handlers.TimedRotatingFileHandler(LOG_FILE, when='h', interval=2)
        fileHandler.setFormatter(formatter)

        # define console handler
        consoleHandler = colorlog.StreamHandler()
        consoleHandler.setFormatter(consoleFormatter)

        self.setLevel(logging.INFO)
        self.addHandler(fileHandler)
        self.addHandler(consoleHandler)


def createLogger(name=None) -> Logger:
    if name:
        return Logger(name)
    else:
        return Logger("PyDNS")


logger = createLogger()
