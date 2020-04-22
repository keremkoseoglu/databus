""" Databus initialization module """
from os import path
from sys import modules

__version__ = "2.1.0"
AUTHOR = "Kerem Koseoglu"
EMAIL = "kerem@keremkoseoglu.com"
DESCRIPTION = "Databus is a framework to transfer data between systems."
PYTHON_VERSION = ">=3.7"


def get_root_path() -> str:
    """ Returns the root path of Databus """
    return path.dirname(modules['__main__'].__file__)
