from config.constants import *
import inspect
from processor.abstract_processor import AbstractProcessor
from typing import List
from utility.file_system import FileSystem


class ProcessorFactory:
    @staticmethod
    def create_processor(p_module: str) -> AbstractProcessor:
        module = __import__(PROCESSOR_PATH + "." + p_module, fromlist=[""])
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name != "AbstractProcessor":
                obj_instance = obj()
                if isinstance(obj_instance, AbstractProcessor):
                    return obj_instance

    @staticmethod
    def get_processor_types() -> List[str]:
        return FileSystem.get_all_python_modules(PROCESSOR_PATH)
