""" Databus initialization module """
from os import path
from sys import modules

__version__ = "8.1.0"
AUTHOR = "Kerem Koseoglu"
EMAIL = "kerem@keremkoseoglu.com"
DESCRIPTION = "Databus is a middleware framework"
PYTHON_VERSION = ">=3.8.2"


def get_root_path() -> str:
    """ Returns the root path of Databus """
    return path.dirname(modules['__main__'].__file__)
