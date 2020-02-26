from abc import ABC, abstractmethod
from client.client_passenger import ClientPassenger
from client.log import Log
from database.abstract_database import AbstractDatabase
from processor.abstract_factory import AbstractProcessorFactory
from pqueue.abstract_factory import AbstractQueueFactory
from pqueue.abstract_queue import AbstractQueue
from puller.abstract_factory import AbstractPullerFactory
from pusher.abstract_factory import AbstractPusherFactory


class BusTicket:
    def __init__(self,
                 p_client_passenger: ClientPassenger = None,
                 p_log: Log = None,
                 p_database: AbstractDatabase = None):

        if p_client_passenger is None:
            self.client_passenger = ClientPassenger()
        else:
            self.client_passenger = p_client_passenger

        if p_log is None:
            self.log = Log()
        else:
            self.log = p_log

        self.database = p_database

    @property
    def client_id(self) -> str:
        return self.database.client.id


class AbstractDriver(ABC):

    def __init__(self,
                 p_queue_factory: AbstractQueueFactory,
                 p_processor_factory: AbstractProcessorFactory,
                 p_puller_factory: AbstractPullerFactory,
                 p_pusher_factory: AbstractPusherFactory):
        self.queue_factory = p_queue_factory
        self.processor_factory = p_processor_factory
        self.puller_factory = p_puller_factory
        self.pusher_factory = p_pusher_factory

    @abstractmethod
    def drive(self, p_bus_ticket: BusTicket):
        pass

    @property
    @abstractmethod
    def queue(self) -> AbstractQueue:
        pass
