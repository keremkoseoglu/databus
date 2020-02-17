from config.constants import *
import inspect
from puller.abstract_puller import AbstractPuller
from typing import List
from utility.file_system import FileSystem


class PullerFactory:
    @staticmethod
    def create_puller(p_module: str) -> AbstractPuller:
        module = __import__(PULLER_PATH + "." + p_module, fromlist=[""])
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name != "AbstractPuller":
                obj_instance = obj()
                if isinstance(obj_instance, AbstractPuller):
                    return obj_instance

    @staticmethod
    def get_puller_types() -> List[str]:
        return FileSystem.get_all_python_modules(PULLER_PATH)