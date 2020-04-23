""" Abstract driver module """
from abc import ABC, abstractmethod
from typing import List
from databus.client.client_passenger import ClientPassenger
from databus.client.log import Log
from databus.database.abstract_database import AbstractDatabase
from databus.passenger.abstract_passenger import AbstractPassenger
from databus.processor.abstract_factory import AbstractProcessorFactory
from databus.pqueue.abstract_factory import AbstractQueueFactory
from databus.pqueue.abstract_queue import AbstractQueue
from databus.puller.abstract_factory import AbstractPullerFactory
from databus.pusher.abstract_factory import AbstractPusherFactory


class BusTicket: # pylint: disable=R0903
    """ Driver constructor parameters """

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
        """ ID of the client """
        return self.database.client.id


class AbstractDriver(ABC):
    """ Abstract driver class """

    def __init__(self,
                 p_queue_factory: AbstractQueueFactory,
                 p_processor_factory: AbstractProcessorFactory,
                 p_puller_factory: AbstractPullerFactory,
                 p_pusher_factory: AbstractPusherFactory):
        self.queue_factory = p_queue_factory
        self.processor_factory = p_processor_factory
        self.puller_factory = p_puller_factory
        self.pusher_factory = p_pusher_factory

    @property
    @abstractmethod
    def queue(self) -> AbstractQueue:
        """ Queue object """

    @abstractmethod
    def drive(self, p_bus_ticket: BusTicket):
        """ Carries passengers from source system to target system """

    def pull_passengers_from_module(self,
                                    p_puller_module: str,
                                    p_log: Log = None) -> List[AbstractPassenger]:
        """ Pulls new passengers from the given puller module """
        if p_log is None:
            log = Log()
        else:
            log = p_log
        puller_obj = self.puller_factory.create_puller(p_puller_module, log)
        return puller_obj.pull()
