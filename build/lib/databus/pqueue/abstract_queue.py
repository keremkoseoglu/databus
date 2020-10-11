""" Abstract queue module """
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime
from databus.client.log import Log
from databus.database.abstract_database import AbstractDatabase
from databus.passenger.abstract_passenger import AbstractPassenger
from databus.pqueue.queue_status import PassengerQueueStatus


class AbstractQueue(ABC):
    """ Abstract queue class """

    def __init__(self, p_database: AbstractDatabase, p_log: Log):
        self.database = p_database
        self.log = p_log

    @abstractmethod
    def delete_completed_passengers(self, p_passenger_module: str, p_pulled_before: datetime):
        """ Deletes completed passengers from the database,
        which were pulled before p_pulled_before and queued, processed, puller-notified, pushed
        """

    @abstractmethod
    def erase(self):
        """ Deletes all passengers from the database """

    @abstractmethod
    def insert(self, p_passengers: List[AbstractPassenger]):
        """ Adds a new passenger to the database """

    @abstractmethod
    def get_deliverable_passengers(self, p_passenger_module: str) -> List[PassengerQueueStatus]:
        """ Returns passengers which can be pushed
        Passengers returned here are pulled, queued, processed and puller-notified,
        but not delivered
        """

    @abstractmethod
    def get_processable_passengers(self, p_passenger_module: str) -> List[PassengerQueueStatus]:
        """ Returns passengers which can be processed
        Passengers returned here are pulled, queued and puller-notified,
        but not processed
        """

    @abstractmethod
    def get_puller_notifiable_passengers(self) -> List[PassengerQueueStatus]:
        """ Returns passengers which have been queued
        Passengers returned here are pulled, queued,
        but not puller-notified
        """

    @abstractmethod
    def update_passenger_status(self, p_status: PassengerQueueStatus):
        """ Updates passenger status """
