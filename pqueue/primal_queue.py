from client.log import Log
from database.abstract_database import AbstractDatabase
from passenger.abstract_passenger import AbstractPassenger
from pqueue.abstract_queue import AbstractQueue
from pqueue.queue_status import QueueStatus
from typing import List


class PrimalQueue(AbstractQueue):

    def __init__(self):
        pass

    def insert(self,
               p_database: AbstractDatabase,
               p_client_id: str,
               p_passengers: List[AbstractPassenger],
               p_log: Log):

        if len(p_passengers) <= 0:
            p_log.append(p_client_id + " için kuyruğa eklenecek veri yok")
            return

        p_log.append(p_client_id + " için kuyruğa eklenecek veriler:")
        for passenger in p_passengers:
            p_log.append(passenger.id_text)

        p_database.insert_passenger_queue(p_passengers=p_passengers,
                                          p_log=p_log)

    def get_undelivered_passengers(self,
                                   p_database: AbstractDatabase,
                                   p_client_id: str,
                                   p_passenger_module: str,
                                   p_log: Log) -> List[AbstractPassenger]:

        p_log.append(p_client_id + " için gönderilmemiş veriler çekiliyor")

        output = p_database.get_passenger_queue_entries(p_status=QueueStatus.undelivered,
                                                        p_passenger_module=p_passenger_module,
                                                        p_log=p_log)

        if len(output) <= 0:
            p_log.append("Gönderilmemiş veri bulunamadı")
        else:
            for undelivered_passenger in output:
                p_log.append("Bulunan veri: " + undelivered_passenger.id_text)

        return output

    def set_passengers_delivered(self,
                                 p_database: AbstractDatabase,
                                 p_client_id: str,
                                 p_passengers: List[AbstractPassenger],
                                 p_log: Log):
        p_log.append(p_client_id + " verileri gönderildi olarak işaretlenecek")

        for delivered_passenger in p_passengers:
            p_log.append("İşaretlenecek veri: " + delivered_passenger.id_text)

        p_database.set_passenger_queue_status(p_passengers=p_passengers,
                                              p_status=QueueStatus.delivered,
                                              p_log=p_log)

        p_log.append("İşaretleme işlemi tamamlandı")
