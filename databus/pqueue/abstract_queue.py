from abc import ABC, abstractmethod
from databus.client.log import Log
from databus.database.abstract_database import AbstractDatabase
from datetime import datetime
from databus.passenger.abstract_passenger import AbstractPassenger
from databus.pqueue.queue_status import PassengerQueueStatus
from typing import List


class AbstractQueue(ABC):

    def __init__(self, p_database: AbstractDatabase, p_log: Log):
        self.database = p_database
        self.log = p_log

    @abstractmethod
    def delete_completed_passengers(self, p_passenger_module: str, p_pulled_before: datetime):
        pass

    @abstractmethod
    def erase(self):
        pass

    @abstractmethod
    def insert(self, p_passengers: List[AbstractPassenger]):
        pass

    @abstractmethod
    def get_deliverable_passengers(self, p_passenger_module: str) -> List[PassengerQueueStatus]:
        pass

    @abstractmethod
    def get_processable_passengers(self, p_passenger_module: str) -> List[PassengerQueueStatus]:
        pass

    @abstractmethod
    def get_puller_notifiable_passengers(self) -> List[PassengerQueueStatus]:
        pass

    @abstractmethod
    def update_passenger_status(self, p_status: PassengerQueueStatus):
        pass
