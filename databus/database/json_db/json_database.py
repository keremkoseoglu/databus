""" Implementation module for JSON database """
from datetime import datetime
from shutil import disk_usage
from typing import List
from uuid import UUID
from databus.client.client import Client
from databus.client.log import Log, LogEntry, MessageType
from databus.client.user import Credential
from databus.client.customizing import ClientCustomizing
from databus.database.abstract_database import AbstractDatabase, LogListItem
from databus.database.json_db.json_client import JsonClient
from databus.database.json_db.json_database_arguments import JsonDatabaseArguments
from databus.database.json_db.json_log import JsonLog
from databus.database.json_db.json_queue import JsonQueue
from databus.database.json_db.json_cust_node_backup import CustomizingNodeBackup
from databus.passenger.abstract_factory import AbstractPassengerFactory
from databus.passenger.abstract_passenger import AbstractPassenger
from databus.pqueue.queue_status import QueueStatus, PassengerQueueStatus

ARGS_TEMPLATE = JsonDatabaseArguments.TEMPLATE

class JsonDatabase(AbstractDatabase):
    """ Implementation class for JSON database """
    _FREE_SPACE_ERROR_PERC = 5

    def __init__(self,
                 p_client_id: str,
                 p_log: Log,
                 p_passenger_factory: AbstractPassengerFactory,
                 p_arguments: dict):
        super().__init__(p_client_id, p_log, p_passenger_factory, p_arguments)
        self._args = JsonDatabaseArguments(p_arguments)
        self._json_client = JsonClient(self._args)
        if p_client_id is None or p_client_id == "":
            self.client = None
        else:
            try:
                self.client = self._get_client(p_client_id)
            except Exception: # pylint: disable=W0703
                self.client = None # We might be creating a new database
        self._json_log = JsonLog(self._args)
        self._json_queue = JsonQueue(p_client_id, p_log, self.passenger_factory, self._args)
        self._cust_node_backup = CustomizingNodeBackup(json_db_arguments=self._args)
        self._check_disk_size(p_log)

    @property
    def client_master_data(self) -> str:
        """ Returns the definition of all clients as a JSON string """
        return self._json_client.client_master_as_json

    @client_master_data.setter
    def client_master_data(self, p_definitions: str):
        """ Sets the definitions into the clients config JSON """
        self._json_client.client_master_as_json = p_definitions

    @property
    def customizing(self) -> str:
        """ Returns the client customizing as JSON """
        return self._json_client.get_config_as_string(self.client_id)

    @customizing.setter
    def customizing(self, p_customizing: str):
        """ Sets the customizing into the clients config JSON """
        self._json_client.save_config(self.client_id, p_customizing)

    def delete_old_logs(self, p_before: datetime):
        """ Deletes old logs from the disk """
        self.log.append_text(f"Deleting logs before {p_before.isoformat()}")
        self._json_log.delete_log_file_before(self.client.id, p_before, self.log)

    def delete_passenger_queue(self, p_passengers: List[AbstractPassenger]):
        """ Deletes passenger from disk """
        self.log.append_text("Deleting passengers from queue")
        self._json_queue.delete_passengers(p_passengers)

    def ensure_schema_existence(self):
        """ Checks the schema for the client
        Creates / completes the schema if anything is missing
        """
        self._json_client.ensure_schema_existence(self.client_id)

    def erase_passenger_queue(self):
        """ Deletes all passengers from disk """
        self.log.append_text("Erasing passenger queue")
        self._json_queue.erase_passenger_queue()

    def get_clients(self) -> List[Client]:
        """ Returns a list of clients """
        return self._json_client.all_clients

    def get_log_content(self, p_log_id: str) -> str:
        """ Returns the contents of the given log
        p_log_id is whatever you have returned in get_log_list.
        """
        return self._json_log.get_log_file_content(self.client_id, p_log_id)

    def get_log_list(self) -> List[LogListItem]:
        """ Returns log entries """
        output = []
        b_warning = f"[{MessageType.warning.name}]"
        b_error = f"[{MessageType.error.name}]"

        log_ids = self._json_log.get_log_file_list(self.client_id)
        for log_id in log_ids:
            output_item = LogListItem(p_log_id=log_id)
            log_content = self.get_log_content(log_id)
            if b_error in log_content:
                output_item.worst_message_type = MessageType.error
            elif b_warning in log_content:
                output_item.worst_message_type = MessageType.warning
            else:
                output_item.worst_message_type = MessageType.info
            output.append(output_item)
        return output

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

    def insert_client(self, p_client: Client):
        """ Inserts a new client """
        self._json_client.create_client_if_missing__by_obj(p_client)

    def insert_log(self, p_log: Log):
        """ Creates a new log file on the disk """
        self.log.append_text("Writing log to disk")
        if self.client is None:
            return
        self._json_log.insert(self.client.id, p_log)

    def insert_passenger_queue(self, p_passenger_status: PassengerQueueStatus):
        """ Writes new files to the disk """
        self.log.append_text(f"Appending passenger {p_passenger_status.passenger.id_text}")
        self._json_queue.insert_passenger(p_passenger_status)

    def update_queue_status(self, p_status: PassengerQueueStatus):
        """ Updates queue files on the disk """
        self.log.append_text(f"Updating passenger {p_status.passenger.id_text}")
        self._json_queue.update_passenger(p_status)

    def update_user_credential(self, p_credential: Credential):
        """ Updates the credential of the given user """
        self._json_client.update_user_credential(self.client_id, p_credential)

    def convert_log_guid_to_id(self, p_guid: UUID) -> str:
        """ UUID to id conversion """
        guid_as_str = str(p_guid)
        log_ids = self._json_log.get_log_file_list(self.client_id)
        for log_id in log_ids:
            if guid_as_str in log_id:
                return log_id
        return ""

    def backup_client_customizing(self, p_cc: ClientCustomizing):
        """ Backup customizing nodes """
        self._cust_node_backup.execute(p_cc=p_cc)

    def delete_old_client_customizing_backups(self, p_before: datetime, p_log: Log):
        """ Deletes overdue client customizing backups """
        self._cust_node_backup.delete_old_files(p_before=p_before, p_db=self, p_log=p_log)

    def _get_client(self, p_id: str) -> Client:
        return self._json_client.get_single(p_id)

    def _check_disk_size(self, p_log: Log):
        total, used, free = disk_usage("/")
        divider = 2**30
        total_gb = total // divider
        used_gb = used // divider
        free_gb = free // divider
        free_perc = int((free / total) * 100)

        p_log.append_text(f"Disk {total_gb}GB, used {used_gb}GB, free {free_gb}GB ({free_perc})%")

        if free_perc <= JsonDatabase._FREE_SPACE_ERROR_PERC:
            size_entry = LogEntry(p_message="Disk space running low", p_type=MessageType.error)
            p_log.append_entry(size_entry)
