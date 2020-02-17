from config.constants import *
import inspect
from passenger.abstract_passenger import AbstractPassenger
from typing import List
from utility.file_system import FileSystem


class PassengerFactory:
    @staticmethod
    def create_passenger(p_module: str) -> AbstractPassenger:
        module = __import__(PASSENGER_PATH + "." + p_module, fromlist=[""])
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name != "AbstractPassenger":
                return obj()

    @staticmethod
    def get_passenger_types() -> List[str]:
        return FileSystem.get_all_python_modules(PASSENGER_PATH)