""" Abstract database module """
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from databus.client.client import Client
from databus.client.log import Log
from databus.passenger.abstract_factory import AbstractPassengerFactory
from databus.passenger.abstract_passenger import AbstractPassenger
from databus.pqueue.queue_status import PassengerQueueStatus, QueueStatus


class AbstractDatabase(ABC):
    """ Abstract database class """
    def __init__(self,
                 p_client_id: str,
                 p_log: Log,
                 p_passenger_factory: AbstractPassengerFactory,
                 p_arguments: dict):
        self.client_id = p_client_id
        self.log = p_log
        self.passenger_factory = p_passenger_factory
        self.arguments = p_arguments
        self.client = Client()

    @abstractmethod
    def delete_old_logs(self, p_before: datetime):
        """ Deletes overdue logs """

    @abstractmethod
    def delete_passenger_queue(self, p_passengers: List[AbstractPassenger]):
        """ Deletes the given passengers from queue """

    @abstractmethod
    def erase_passenger_queue(self):
        """ Eradicates queue completely """

    @abstractmethod
    def get_clients(self) -> List[Client]:
        """ Returns clients """

    @abstractmethod
    def get_log_content(self, p_log_id: str) -> str:
        """ Returns the contents of the given log
        p_log_id is whatever you have returned in get_log_list.
        """

    @abstractmethod
    def get_log_list(self) -> List[str]:
        """ Returns a list of log files """

    @abstractmethod
    def get_passenger_queue_entries(self, # pylint: disable=R0913
                                    p_passenger_module: str = None,
                                    p_processor_status: QueueStatus = None,
                                    p_pusher_status: QueueStatus = None,
                                    p_puller_notified: bool = None,
                                    p_pulled_before: datetime = None
                                    ) -> List[PassengerQueueStatus]:
        """ Returns requested passenger queue entries """

    @abstractmethod
    def get_passenger_queue_entry(self, # pylint: disable=R0913
                                  p_internal_id: str
                                 ) -> PassengerQueueStatus:
        """ Returns requested passenger queue entry """

    @abstractmethod
    def insert_log(self, p_log: Log):
        """ Inserts new log entries """

    @abstractmethod
    def insert_passenger_queue(self, p_passenger_status: PassengerQueueStatus):
        """ Adds the to queue """

    @abstractmethod
    def update_queue_status(self, p_status: PassengerQueueStatus):
        """ Updates the status of the passenger in the queue """

    @abstractmethod
    def _get_client(self, p_id: str) -> Client:
        """ Returns a new client """
