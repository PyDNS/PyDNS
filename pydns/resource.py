import os
import sys


def isFrozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")


def getWriteableResourcePath():
    """
    Returns a path that contains configuration files for the application
    """
    if isFrozen():
        return os.getcwd()
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
