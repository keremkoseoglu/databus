from abc import ABC, abstractmethod
from config.constants import *
from database.abstract_factory import AbstractDatabaseFactory
from driver.abstract_factory import AbstractDriverFactory
from passenger.abstract_factory import AbstractPassengerFactory
from pqueue.abstract_factory import AbstractQueueFactory
from puller.abstract_factory import AbstractPullerFactory
from pusher.abstract_factory import AbstractPusherFactory
from processor.abstract_factory import AbstractProcessorFactory


class DispatcherTicket:
    def __init__(self,
                 p_database_factory: AbstractDatabaseFactory,
                 p_driver_factory: AbstractDriverFactory,
                 p_passenger_factory: AbstractPassengerFactory,
                 p_queue_factory: AbstractQueueFactory,
                 p_puller_factory: AbstractPullerFactory,
                 p_processor_factory: AbstractProcessorFactory,
                 p_pusher_factory: AbstractPusherFactory,
                 p_database_module: str = DATABASE_DEFAULT,
                 p_driver_module: str = DRIVER_DEFAULT
                 ):
        self.database_factory = p_database_factory
        self.driver_factory = p_driver_factory
        self.passenger_factory = p_passenger_factory
        self.queue_factory = p_queue_factory
        self.puller_factory = p_puller_factory
        self.processor_factory = p_processor_factory
        self.pusher_factory = p_pusher_factory
        self.database_module = p_database_module
        self.driver_module = p_driver_module


class AbstractDispatcher(ABC):
    def __init__(self, p_ticket: DispatcherTicket = None):
        self.ticket = p_ticket

    @abstractmethod
    def start(self):
        pass
