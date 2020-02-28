import os
import sys

# All supported db
BACKENDS = ['mysql', 'postgresql', 'file']


def getConfigPath():
    return os.getcwd()


def isFrozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")


def getWriteableResourcePath():
    """
    Returns a path that contains configuration files for the application
    """
    return os.getcwd()


def getVersion():
    # todo: make this dynamic
    return '1.0.0'
