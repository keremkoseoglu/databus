from abc import ABC, abstractmethod
from databus.database.abstract_factory import AbstractDatabaseFactory
from databus.driver.abstract_factory import AbstractDriverFactory
from databus.passenger.abstract_factory import AbstractPassengerFactory
from databus.pqueue.abstract_factory import AbstractQueueFactory
from databus.puller.abstract_factory import AbstractPullerFactory
from databus.pusher.abstract_factory import AbstractPusherFactory
from databus.processor.abstract_factory import AbstractProcessorFactory


class DispatcherTicket:
    def __init__(self,
                 p_database_factory: AbstractDatabaseFactory,
                 p_driver_factory: AbstractDriverFactory,
                 p_passenger_factory: AbstractPassengerFactory,
                 p_queue_factory: AbstractQueueFactory,
                 p_puller_factory: AbstractPullerFactory,
                 p_processor_factory: AbstractProcessorFactory,
                 p_pusher_factory: AbstractPusherFactory,
                 p_database_module: str = None,
                 p_database_arguments: dict = None,
                 p_driver_module: str = None
                 ):
        self.database_factory = p_database_factory
        self.driver_factory = p_driver_factory
        self.passenger_factory = p_passenger_factory
        self.queue_factory = p_queue_factory
        self.puller_factory = p_puller_factory
        self.processor_factory = p_processor_factory
        self.pusher_factory = p_pusher_factory
        self.driver_module = p_driver_module

        if p_database_module is None:
            self.database_module = ""
        else:
            self.database_module = p_database_module

        if p_database_arguments is None:
            self.database_arguments = {}
        else:
            self.database_arguments = p_database_arguments

        if p_driver_module is None:
            self.driver_module = ""
        else:
            self.driver_module = p_driver_module


class AbstractDispatcher(ABC):
    def __init__(self, p_ticket: DispatcherTicket = None):
        self.ticket = p_ticket

    @abstractmethod
    def start(self):
        pass
