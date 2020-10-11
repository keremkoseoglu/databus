""" Default processor factory module """
from vibhaga.inspector import Inspector
from databus.client.log import Log
from databus.processor.abstract_factory import AbstractProcessorFactory, ProcessorCreationError
from databus.processor.abstract_processor import AbstractProcessor


class PrimalProcessorFactory(AbstractProcessorFactory): # pylint: disable=R0903
    """ Default processor factory class """

    def create_processor(self, p_module: str, p_log: Log) -> AbstractProcessor:
        """ Factory method """
        if p_module == "" or p_module is None:
            raise ProcessorCreationError(ProcessorCreationError.ErrorCode.parameter_missing)

        candidates = Inspector.get_classes_in_module(
            p_module,
            exclude_classes=["AbstractProcessor"])

        for candidate in candidates:
            try:
                obj_instance = candidate(p_log)
                if isinstance(obj_instance, AbstractProcessor):
                    return obj_instance
            except Exception: # pylint: disable=W0703
                pass

        raise ProcessorCreationError(
            ProcessorCreationError.ErrorCode.cant_create_instance,
            p_module=p_module)
