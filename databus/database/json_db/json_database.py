""" Implementation module for JSON database """
from datetime import datetime
from typing import List
from databus.client.client import Client
from databus.client.log import Log
from databus.database.abstract_database import AbstractDatabase
from databus.database.json_db.json_client import JsonClient
from databus.database.json_db.json_database_arguments import JsonDatabaseArguments
from databus.database.json_db.json_log import JsonLog
from databus.database.json_db.json_queue import JsonQueue
from databus.passenger.abstract_factory import AbstractPassengerFactory
from databus.passenger.abstract_passenger import AbstractPassenger
from databus.pqueue.queue_status import QueueStatus, PassengerQueueStatus


class JsonDatabase(AbstractDatabase):
    """ Implementation class for JSON database """
    def __init__(self,
                 p_client_id: str,
                 p_log: Log,
                 p_passenger_factory: AbstractPassengerFactory,
                 p_arguments: dict):
        super().__init__(p_client_id, p_log, p_passenger_factory, p_arguments)
        self._args = JsonDatabaseArguments(p_arguments)
        self._json_client = JsonClient(self._args)
        if p_client_id is None:
            self.client = None
        else:
            self.client = self._get_client(p_client_id)
        self._json_log = JsonLog(self._args)
        self._json_queue = JsonQueue(p_client_id, p_log, self.passenger_factory, self._args)

    def delete_old_logs(self, p_before: datetime):
        """ Deletes old logs from the disk """
        self.log.append_text("Deleting logs before " + p_before.isoformat())
        self._json_log.delete_log_file_before(self.client.id, p_before, self.log)

    def delete_passenger_queue(self, p_passengers: List[AbstractPassenger]):
        """ Deletes passenger from disk """
        self.log.append_text("Deleting passengers from queue")
        self._json_queue.delete_passengers(p_passengers)

    def erase_passenger_queue(self):
        """ Deletes all passengers from disk """
        self.log.append_text("Erasing passenger queue")
        self._json_queue.erase_passenger_queue()

    def get_clients(self) -> List[Client]:
        """ Returns a single client """
        return self._json_client.get_all()

    def get_log_content(self, p_log_id: str) -> str:
        """ Returns the contents of the given log
        p_log_id is whatever you have returned in get_log_list.
        """
        return self._json_log.get_log_file_content(self.client_id, p_log_id)

    def get_log_list(self) -> List[str]:
        """ Returns log entries """
        return self._json_log.get_log_file_list(self.client_id)

    def get_passenger_queue_entries(self, # pylint: disable=R0913
                                    p_passenger_module: str = None,
                                    p_processor_status: QueueStatus = None,
                                    p_pusher_status: QueueStatus = None,
                                    p_puller_notified: bool = None,
                                    p_pulled_before: datetime = None
                                    ) -> List[PassengerQueueStatus]:
        """ Reads the requested entries from the disk """
        self.log.append_text("Reading passenger queue entries")

        return self._json_queue.get_passengers(p_passenger_module,
                                               p_processor_status,
                                               p_pusher_status,
                                               p_puller_notified,
                                               p_pulled_before)

    def get_passenger_queue_entry(self, # pylint: disable=R0913
                                  p_internal_id: str
                                 ) -> PassengerQueueStatus:
        return self._json_queue.get_passengers(p_internal_id=p_internal_id)[0]

    def insert_log(self, p_log: Log):
        """ Creates a new log file on the disk """
        self.log.append_text("Writing log to disk")
        self._json_log.insert(self.client.id, p_log)

    def insert_passenger_queue(self, p_passenger_status: PassengerQueueStatus):
        """ Writes new files to the disk """
        self.log.append_text("Appending passenger " + p_passenger_status.passenger.id_text)
        self._json_queue.insert_passenger(p_passenger_status)

    def update_queue_status(self, p_status: PassengerQueueStatus):
        """ Updates queue files on the disk """
        self.log.append_text("Updating passenger " + p_status.passenger.id_text)
        self._json_queue.update_passenger(p_status)

    def _get_client(self, p_id: str) -> Client:
        return self._json_client.get_single(p_id)
