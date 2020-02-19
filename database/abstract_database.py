from abc import ABC, abstractmethod
from client.client import Client
from client.log import Log
from datetime import datetime
from passenger.abstract_passenger import AbstractPassenger
from pqueue.queue_status import QueueStatus
from typing import List


class AbstractDatabase(ABC):

    client: Client

    def __init__(self, p_client_id: str):
        self.client = self._get_client(p_client_id)

    @abstractmethod
    def delete_old_logs(self, p_before: datetime):
        pass

    @abstractmethod
    def delete_passenger_queue(self, p_passengers: List[AbstractPassenger], p_log: Log):
        pass

    @abstractmethod
    def get_clients(self) -> List[Client]:
        pass

    @abstractmethod
    def get_passenger_queue_entries(self,
                                    p_status: QueueStatus,
                                    p_passenger_module: str,
                                    p_log: Log) -> List[AbstractPassenger]:
        pass

    @abstractmethod
    def insert_log(self, p_log: Log):
        pass

    @abstractmethod
    def insert_passenger_queue(self, p_passengers: List[AbstractPassenger], p_log: Log):
        pass

    @abstractmethod
    def set_passenger_queue_status(self, p_passengers: List[AbstractPassenger], p_status: QueueStatus, p_log: Log):
        pass

    @abstractmethod
    def _get_client(self, p_id: str) -> Client:
        pass
