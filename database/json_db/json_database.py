from client.client import Client
from client.log import Log
from database.abstract_database import AbstractDatabase
from database.json_db.json_client import JsonClient
from database.json_db.json_log import JsonLog
from database.json_db.json_queue import JsonQueue
from datetime import datetime
from passenger.abstract_factory import AbstractPassengerFactory
from passenger.abstract_passenger import AbstractPassenger
from pqueue.queue_status import QueueStatus, PassengerQueueStatus
from typing import List


class JsonDatabase(AbstractDatabase):
    def __init__(self,
                 p_client_id: str,
                 p_log: Log,
                 p_passenger_factory: AbstractPassengerFactory):
        super().__init__(p_client_id, p_log, p_passenger_factory)
        self.__json_queue = JsonQueue(p_client_id, p_log, self.passenger_factory)

    def delete_old_logs(self, p_before: datetime):
        self.log.append_text("Deleting logs before " + p_before.isoformat())
        JsonLog.delete_log_file_before(self.client.id, p_before, self.log)

    def delete_passenger_queue(self, p_passengers: List[AbstractPassenger]):
        self.log.append_text("Deleting passengers from queue")
        self.__json_queue.delete_passengers(p_passengers)

    def erase_passsenger_queue(self):
        self.log.append_text("Erasing passenger queue")
        self.__json_queue.erase_passenger_queue()

    def get_clients(self) -> List[Client]:
        return JsonClient.get_all()

    def get_passenger_queue_entries(self,
                                    p_passenger_module: str = None,
                                    p_processor_status: QueueStatus = None,
                                    p_pusher_status: QueueStatus = None,
                                    p_puller_notified: bool = None
                                    ) -> List[PassengerQueueStatus]:

        self.log.append_text("Reading passenger queue entries")

        return self.__json_queue.get_passengers(p_passenger_module,
                                                p_processor_status,
                                                p_pusher_status,
                                                p_puller_notified)

    def insert_log(self, p_log: Log):
        self.log.append_text("Writing log to disk")
        JsonLog.insert(self.client.id, p_log)

    def insert_passenger_queue(self, p_passenger_status: PassengerQueueStatus):
        self.log.append_text("Appending passenger " + p_passenger_status.passenger.id_text)
        self.__json_queue.insert_passenger(p_passenger_status)

    def update_queue_status(self, p_status: PassengerQueueStatus):
        self.log.append_text("Updating passenger " + p_status.passenger.id_text)
        self.__json_queue.update_passenger(p_status)

    def _get_client(self, p_id: str) -> Client:
        return JsonClient.get_single(p_id)
