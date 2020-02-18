from config.constants import *
import inspect
from pusher.abstract_pusher import AbstractPusher
from typing import List
from utility.file_system import FileSystem


class PusherFactory:
    @staticmethod
    def create_pusher(p_module: str) -> AbstractPusher:
        module = __import__(PUSHER_PATH + "." + p_module, fromlist=[""])
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name != "AbstractPusher":
                obj_instance = obj()
                if isinstance(obj_instance, AbstractPusher):
                    return obj_instance

    @staticmethod
    def get_pusher_types() -> List[str]:
        return FileSystem.get_all_python_modules(PUSHER_PATH)
