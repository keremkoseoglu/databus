from client.client import Client
from client.log import Log
from database.abstract_database import AbstractDatabase
from database.json_db.json_client import JsonClient
from database.json_db.json_log import JsonLog
from database.json_db.json_queue import JsonQueue
from datetime import datetime
from passenger.abstract_passenger import AbstractPassenger
from pqueue.queue_status import QueueStatus
from typing import List


class JsonDatabase(AbstractDatabase):

    def __init__(self, p_client_id: str):
        super().__init__(p_client_id)

    def delete_old_logs(self, p_before: datetime):
        # todo
        # log içerisinde yordam açıp tamamla
        # buradan log yordamını çağır
        # tamamla
        # test ekle (münferit log silmek için; test sırasında iki log yarat birini sil)
        # aşağıdaki pass'i sil
        pass

    def delete_passenger_queue(self, p_passengers: List[AbstractPassenger], p_log: Log):
        JsonQueue.delete_passengers(p_passengers=p_passengers, p_log=p_log)

    def get_clients(self) -> List[Client]:
        return JsonClient.get_all()

    def get_passenger_queue_entries(self,
                                    p_status: QueueStatus,
                                    p_passenger_module: str,
                                    p_log: Log) -> List[AbstractPassenger]:

        return JsonQueue(p_client_id=self.client.id).get_passengers(p_status=p_status,
                                                                    p_passenger_module=p_passenger_module,
                                                                    p_log=p_log)

    def insert_log(self, p_log: Log):
        JsonLog.insert(p_client_id=self.client.id, p_log=p_log)

    def insert_passenger_queue(self, p_passengers: List[AbstractPassenger], p_log: Log):
        JsonQueue(p_client_id=self.client.id).insert_passengers(p_passengers=p_passengers, p_log=p_log)

    def set_passenger_queue_status(self, p_passengers: List[AbstractPassenger], p_status: QueueStatus, p_log: Log):
        JsonQueue(p_client_id=self.client.id).set_passenger_status(
            p_passengers=p_passengers,
            p_status=p_status,
            p_log=p_log)

    def _get_client(self, p_id: str) -> Client:
        return JsonClient.get_single(p_id)