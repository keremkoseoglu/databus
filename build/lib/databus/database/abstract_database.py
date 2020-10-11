""" Abstract database module """
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from uuid import UUID
from databus.client.client import Client
from databus.client.log import Log, MessageType
from databus.client.user import Credential
from databus.passenger.abstract_factory import AbstractPassengerFactory
from databus.passenger.abstract_passenger import AbstractPassenger
from databus.pqueue.queue_status import PassengerQueueStatus, QueueStatus


class LogListItem: # pylint: disable=R0903
    """ A structure for a log list item """
    def __init__(self,
                 p_log_id: str = "",
                 p_worst_message_type: MessageType = MessageType.info):
        self.log_id = p_log_id
        self.worst_message_type = p_worst_message_type


class AbstractDatabase(ABC):
    """ Abstract database class """
    def __init__(self,
                 p_client_id: str,
                 p_log: Log,
                 p_passenger_factory: AbstractPassengerFactory,
                 p_arguments: dict):
        self.client_id = p_client_id
        self.log = p_log
        self.passenger_factory = p_passenger_factory
        self.arguments = p_arguments
        self.client = Client()

    @property
    @abstractmethod
    def client_master_data(self) -> str:
        """ Returns the definition of all clients as a string
        This string (preferably JSON) will be shown to the
        root user as a JSON file.
        When edited, it will be set back
        """

    @client_master_data.setter
    @abstractmethod
    def client_master_data(self, p_definitions: str):
        """ Sets the definitions returned from the GUI
        Subclasses are expected to write those definitions
        to the disk, database, etc
        """

    @property
    @abstractmethod
    def customizing(self) -> str:
        """ Returns the client customizing in text format
        (preferably JSON)
        """

    @customizing.setter
    @abstractmethod
    def customizing(self, p_customizing: str):
        """ Sets the customizing returned from the GUI
        Subclasses are expected to write those settings
        to the disk, database, etc
        """

    @abstractmethod
    def delete_old_logs(self, p_before: datetime):
        """ Deletes overdue logs """

    @abstractmethod
    def delete_passenger_queue(self, p_passengers: List[AbstractPassenger]):
        """ Deletes the given passengers from queue """

    @abstractmethod
    def ensure_schema_existence(self):
        """ Checks the schema for the client
        Creates / completes the schema if anything is missing
        """

    @abstractmethod
    def erase_passenger_queue(self):
        """ Eradicates queue completely """

    @abstractmethod
    def get_clients(self) -> List[Client]:
        """ Returns clients """

    @abstractmethod
    def get_log_content(self, p_log_id: str) -> str:
        """ Returns the contents of the given log
        p_log_id is whatever you have returned in get_log_list.
        """

    @abstractmethod
    def get_log_list(self) -> List[LogListItem]:
        """ Returns a list of log files """

    @abstractmethod
    def get_passenger_queue_entries(self, # pylint: disable=R0913
                                    p_passenger_module: str = None,
                                    p_processor_status: QueueStatus = None,
                                    p_pusher_status: QueueStatus = None,
                                    p_puller_notified: bool = None,
                                    p_pulled_before: datetime = None
                                    ) -> List[PassengerQueueStatus]:
        """ Returns requested passenger queue entries """

    @abstractmethod
    def get_passenger_queue_entry(self, # pylint: disable=R0913
                                  p_internal_id: str
                                 ) -> PassengerQueueStatus:
        """ Returns requested passenger queue entry """

    @abstractmethod
    def insert_client(self, p_client: Client):
        """ Inserts a new client """

    @abstractmethod
    def insert_log(self, p_log: Log):
        """ Inserts new log entries """

    @abstractmethod
    def insert_passenger_queue(self, p_passenger_status: PassengerQueueStatus):
        """ Adds the to queue """

    @abstractmethod
    def update_queue_status(self, p_status: PassengerQueueStatus):
        """ Updates the status of the passenger in the queue """

    @abstractmethod
    def update_user_credential(self, p_credential: Credential):
        """ Updates the credential of the given user """

    @abstractmethod
    def convert_log_guid_to_id(self, p_guid: UUID) -> str:
        """ UUID to id conversion """

    @abstractmethod
    def _get_client(self, p_id: str) -> Client:
        """ Returns a new client """
