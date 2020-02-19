from abc import ABC, abstractmethod
from client.log import Log
from database.abstract_database import AbstractDatabase
from passenger.abstract_passenger import AbstractPassenger
from typing import List


class AbstractQueue(ABC):

    def __init__(self):
        # todo
        # tüm queue'yu temizleyecek yordam yaz (dosyaları filan da silsin)
        # testlerin başında bunu çağır
        pass

    @abstractmethod
    def insert(self,
               p_database: AbstractDatabase,
               p_client_id: str,
               p_passengers: List[AbstractPassenger],
               p_log: Log):
        pass

    @abstractmethod
    def get_undelivered_passengers(self,
                                   p_database: AbstractDatabase,
                                   p_client_id: str,
                                   p_passenger_module: str,
                                   p_log: Log) -> List[AbstractPassenger]:
        pass

    @abstractmethod
    def set_passengers_delivered(self,
                                 p_database: AbstractDatabase,
                                 p_client_id: str,
                                 p_passengers: List[AbstractPassenger],
                                 p_log: Log):
        pass
