from abc import ABC, abstractmethod
from client.log import Log
from passenger.abstract_passenger import AbstractPassenger
from typing import List


class AbstractPuller(ABC):
    def __init__(self):
        # todo
        # log'u burada
        # aşağıdaki yordamlarda sil
        # uygulayan sınıflarda buna göre kod yaz
        # çağıran yerlerde düzenle
        pass

    @abstractmethod
    def notify_passengers_seated(self, p_seated_passengers: List[AbstractPassenger], p_log: Log):
        pass

    @abstractmethod
    def pull(self, p_log: Log) -> List[AbstractPassenger]:
        pass
