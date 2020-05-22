""" Default driver factory module """
from vibhaga.inspector import Inspector
from databus.driver.abstract_driver import AbstractDriver
from databus.driver.abstract_factory import AbstractDriverFactory, DriverCreationError
from databus.pqueue.abstract_factory import AbstractQueueFactory
from databus.processor.abstract_factory import AbstractProcessorFactory
from databus.puller.abstract_factory import AbstractPullerFactory
from databus.pusher.abstract_factory import AbstractPusherFactory


class PrimalDriverFactory(AbstractDriverFactory): # pylint: disable=R0903
    """ Default driver factory class """

    def create_driver(self, # pylint: disable=R0913
                      p_module: str,
                      p_queue_factory: AbstractQueueFactory,
                      p_processor_factory: AbstractProcessorFactory,
                      p_puller_factory: AbstractPullerFactory,
                      p_pusher_factory: AbstractPusherFactory
                      ) -> AbstractDriver:
        """ Creates a new driver object """
        if p_module == "" or p_module is None:
            raise DriverCreationError(DriverCreationError.ErrorCode.parameter_missing)

        candidates = Inspector.get_classes_in_module(p_module, exclude_classes=["AbstractDriver"])
        for candidate in candidates:
            try:
                obj_instance = candidate(
                    p_queue_factory,
                    p_processor_factory,
                    p_puller_factory,
                    p_pusher_factory)
                if isinstance(obj_instance, AbstractDriver):
                    return obj_instance
            except Exception: # pylint: disable=W0703
                pass

        raise DriverCreationError(
            DriverCreationError.ErrorCode.cant_create_instance,
            p_module=p_module)
