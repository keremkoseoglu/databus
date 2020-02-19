import inspect
from processor.abstract_processor import AbstractProcessor


class ProcessorFactory:
    @staticmethod
    def create_processor(p_module: str) -> AbstractProcessor:
        # todo: factory'leri dolaş, gereksiz import'lar kalmış olabilir
        module = __import__(p_module, fromlist=[""])
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if name != "AbstractProcessor":
                obj_instance = obj()
                if isinstance(obj_instance, AbstractProcessor):
                    return obj_instance

