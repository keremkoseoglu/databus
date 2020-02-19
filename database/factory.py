import inspect
from database.abstract_database import AbstractDatabase


class DatabaseFactory:
    @staticmethod
    def create_database(p_module: str, p_client_id: str) -> AbstractDatabase:
        module = __import__(p_module, fromlist=[""])
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name != "AbstractDatabase":
                try:
                    obj_instance = obj(p_client_id)
                    if isinstance(obj_instance, AbstractDatabase):
                        return obj_instance
                except:
                    continue
        return None # TODO: Burada Exception dönse daha iyi


