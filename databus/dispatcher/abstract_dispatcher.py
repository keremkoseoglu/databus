from abc import ABC, abstractmethod
from databus.database.abstract_factory import AbstractDatabaseFactory
from databus.database.json_db.json_database_arguments import JsonDatabaseArguments
from databus.database.primal_factory import PrimalDatabaseFactory
from databus.driver.abstract_factory import AbstractDriverFactory
from databus.driver.primal_factory import PrimalDriverFactory
from databus.passenger.abstract_factory import AbstractPassengerFactory
from databus.passenger.primal_factory import PrimalPassengerFactory
from databus.pqueue.abstract_factory import AbstractQueueFactory
from databus.pqueue.primal_factory import PrimalQueueFactory
from databus.puller.abstract_factory import AbstractPullerFactory
from databus.puller.primal_factory import PrimalPullerFactory
from databus.pusher.abstract_factory import AbstractPusherFactory
from databus.pusher.primal_factory import PrimalPusherFactory
from databus.processor.abstract_factory import AbstractProcessorFactory
from databus.processor.primal_factory import PrimalProcessorFactory


class DispatcherTicket:
    _DEFAULT_DRIVER = "databus.driver.primal_driver"
    _DEFAULT_DATABASE = "databus.database.json_db.json_database"
    _DEFAULT_DATABASE_ARGS = {
        JsonDatabaseArguments.KEY_CLIENT_CONFIG: "config.json",
        JsonDatabaseArguments.KEY_CLIENT_DIR: "clients",
        JsonDatabaseArguments.KEY_DATABASE_DIR: "data/json_db",
        JsonDatabaseArguments.KEY_LOG_DIR: "log",
        JsonDatabaseArguments.KEY_LOG_EXTENSION: "txt",
        JsonDatabaseArguments.KEY_QUEUE_ATTACHMENT_DIR: "attachments",
        JsonDatabaseArguments.KEY_QUEUE_DIR: "pqueue",
        JsonDatabaseArguments.KEY_QUEUE_PASSENGER: "passenger.json"
    }

    def __init__(self,
                 p_database_factory: AbstractDatabaseFactory = None,
                 p_driver_factory: AbstractDriverFactory = None,
                 p_passenger_factory: AbstractPassengerFactory = None,
                 p_queue_factory: AbstractQueueFactory = None,
                 p_puller_factory: AbstractPullerFactory = None,
                 p_processor_factory: AbstractProcessorFactory = None,
                 p_pusher_factory: AbstractPusherFactory = None,
                 p_database_module: str = None,
                 p_database_arguments: dict = None,
                 p_driver_module: str = None
                 ):

        if p_database_factory is None:
            self.database_factory = PrimalDatabaseFactory()
        else:
            self.database_factory = p_database_factory

        if p_driver_factory is None:
            self.driver_factory = PrimalDriverFactory()
        else:
            self.driver_factory = p_driver_factory

        if p_passenger_factory is None:
            self.passenger_factory = PrimalPassengerFactory()
        else:
            self.passenger_factory = p_passenger_factory

        if p_queue_factory is None:
            self.queue_factory = PrimalQueueFactory()
        else:
            self.queue_factory = p_queue_factory

        if p_puller_factory is None:
            self.puller_factory = PrimalPullerFactory()
        else:
            self.puller_factory = p_puller_factory

        if p_processor_factory is None:
            self.processor_factory = PrimalProcessorFactory()
        else:
            self.processor_factory = p_processor_factory

        if p_pusher_factory is None:
            self.pusher_factory = PrimalPusherFactory()
        else:
            self.pusher_factory = p_pusher_factory

        if p_database_module is None:
            self.database_module = DispatcherTicket._DEFAULT_DATABASE
        else:
            self.database_module = p_database_module

        if p_database_arguments is None:
            self.database_arguments = DispatcherTicket._DEFAULT_DATABASE_ARGS
        else:
            self.database_arguments = p_database_arguments

        if p_driver_module is None:
            self.driver_module = DispatcherTicket._DEFAULT_DRIVER
        else:
            self.driver_module = p_driver_module


class AbstractDispatcher(ABC):
    def __init__(self, p_ticket: DispatcherTicket = None):
        self.ticket = p_ticket

    @abstractmethod
    def start(self):
        pass
