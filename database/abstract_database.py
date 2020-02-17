from abc import ABC, abstractmethod
from client.client import Client
from client.log import Log
from datetime import datetime
from typing import List


class AbstractDatabase(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def delete_old_logs(self, p_before: datetime):
        pass

    @abstractmethod
    def get_client(self, p_name: str) -> Client:
        pass

    @abstractmethod
    def get_clients(self) -> List[Client]:
        pass

    @abstractmethod
    def insert_log(self, p_client: Client, p_log: Log):
        pass


