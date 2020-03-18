from abc import ABC, abstractmethod
from databus.client.client import Client
from databus.client.log import Log
from datetime import datetime
from databus.passenger.abstract_factory import AbstractPassengerFactory
from databus.passenger.abstract_passenger import AbstractPassenger
from databus.pqueue.queue_status import PassengerQueueStatus, QueueStatus
from typing import List


class AbstractDatabase(ABC):
    def __init__(self, p_client_id: str, p_log: Log, p_passenger_factory: AbstractPassengerFactory):
        self.log = p_log
        self.passenger_factory = p_passenger_factory

        if p_client_id is None:
            self.client = None
        else:
            self.client = self._get_client(p_client_id)

    @abstractmethod
    def delete_old_logs(self, p_before: datetime):
        pass

    @abstractmethod
    def delete_passenger_queue(self, p_passengers: List[AbstractPassenger]):
        pass

    @abstractmethod
    def erase_passsenger_queue(self):
        pass

    @abstractmethod
    def get_clients(self) -> List[Client]:
        pass

    @abstractmethod
    def get_passenger_queue_entries(self,
                                    p_passenger_module: str = None,
                                    p_processor_status: QueueStatus = None,
                                    p_pusher_status: QueueStatus = None,
                                    p_puller_notified: bool = None,
                                    p_pulled_before: datetime = None
                                    ) -> List[PassengerQueueStatus]:
        pass

    @abstractmethod
    def insert_log(self, p_log: Log):
        pass

    @abstractmethod
    def insert_passenger_queue(self, p_passenger_status: PassengerQueueStatus):
        pass

    @abstractmethod
    def update_queue_status(self, p_status: PassengerQueueStatus):
        pass

    @abstractmethod
    def _get_client(self, p_id: str) -> Client:
        pass
