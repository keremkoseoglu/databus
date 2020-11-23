""" Databus initialization module """
from os import path
from sys import modules

__version__ = "7.0.0"
AUTHOR = "Kerem Koseoglu"
EMAIL = "kerem@keremkoseoglu.com"
DESCRIPTION = "Databus is a framework to transfer data between systems."
PYTHON_VERSION = ">=3.6.5"


def get_root_path() -> str:
    """ Returns the root path of Databus """
    return path.dirname(modules['__main__'].__file__)
