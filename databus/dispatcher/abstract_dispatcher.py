""" Abstract dispatcher module """
from abc import ABC, abstractmethod
from typing import List
from databus.client.client import Client
from databus.client.external_config import ExternalConfigFile, ExternalConfigFileManager
from databus.client.log import Log
from databus.client.customizing import ClientCustomizing, CustomizingNode
from databus.database.abstract_database import AbstractDatabase
from databus.database.abstract_factory import AbstractDatabaseFactory
from databus.database.json_db.json_database_arguments import JsonDatabaseArguments
from databus.database.primal_factory import PrimalDatabaseFactory
from databus.dispatcher.observer import DispatcherObserver
from databus.driver.abstract_factory import AbstractDriverFactory
from databus.driver.abstract_driver import AbstractDriver
from databus.driver.primal_factory import PrimalDriverFactory
from databus.passenger.abstract_factory import AbstractPassengerFactory
from databus.passenger.primal_factory import PrimalPassengerFactory
from databus.pqueue.abstract_factory import AbstractQueueFactory
from databus.pqueue.primal_factory import PrimalQueueFactory
from databus.puller.abstract_factory import AbstractPullerFactory
from databus.puller.primal_factory import PrimalPullerFactory
from databus.pusher.abstract_factory import AbstractPusherFactory
from databus.pusher.primal_factory import PrimalPusherFactory
from databus.processor.abstract_factory import AbstractProcessorFactory
from databus.processor.primal_factory import PrimalProcessorFactory

CLIENTS_DB_NODE = "__clients__"
DATABUS_DB_NODE = "__databus__"

class DispatcherTicket: # pylint: disable=R0902, R0903
    """ Factory parameters for dispatcher creation """
    _DEFAULT_DRIVER = "databus.driver.primal_driver"
    _DEFAULT_DATABASE = "databus.database.json_db.json_database"
    _DEFAULT_DATABASE_ARGS = {
        JsonDatabaseArguments.KEY_CLIENT_CONFIG: "config.json",
        JsonDatabaseArguments.KEY_CLIENT_DIR: "clients",
        JsonDatabaseArguments.KEY_DATABASE_DIR: "data|json_db",
        JsonDatabaseArguments.KEY_LOG_DIR: "log",
        JsonDatabaseArguments.KEY_LOG_EXTENSION: "txt",
        JsonDatabaseArguments.KEY_QUEUE_ATTACHMENT_DIR: "attachments",
        JsonDatabaseArguments.KEY_QUEUE_DIR: "pqueue",
        JsonDatabaseArguments.KEY_QUEUE_PASSENGER: "passenger.json",
        JsonDatabaseArguments.KEY_BACKUP_DIR: "backup"
    }

    def __init__(self,
                 p_database_factory: AbstractDatabaseFactory = None,
                 p_driver_factory: AbstractDriverFactory = None,
                 p_passenger_factory: AbstractPassengerFactory = None,
                 p_queue_factory: AbstractQueueFactory = None,
                 p_puller_factory: AbstractPullerFactory = None,
                 p_processor_factory: AbstractProcessorFactory = None,
                 p_pusher_factory: AbstractPusherFactory = None,
                 p_database_module: str = None,
                 p_database_arguments: dict = None,
                 p_driver_module: str = None,
                 p_dispatcher_observer: DispatcherObserver = None,
                 p_run_web_server: bool = True,
                 p_web_server_port: int = 5000,
                 p_external_config_files: List[ExternalConfigFile] = None,
                 p_system_alias: str = None
                 ): # pylint: disable=R0912, R0913, R0915, R0914

        if p_database_factory is None:
            self.database_factory = PrimalDatabaseFactory()
        else:
            self.database_factory = p_database_factory

        if p_driver_factory is None:
            self.driver_factory = PrimalDriverFactory()
        else:
            self.driver_factory = p_driver_factory

        if p_passenger_factory is None:
            self.passenger_factory = PrimalPassengerFactory()
        else:
            self.passenger_factory = p_passenger_factory

        if p_queue_factory is None:
            self.queue_factory = PrimalQueueFactory()
        else:
            self.queue_factory = p_queue_factory

        if p_puller_factory is None:
            self.puller_factory = PrimalPullerFactory()
        else:
            self.puller_factory = p_puller_factory

        if p_processor_factory is None:
            self.processor_factory = PrimalProcessorFactory()
        else:
            self.processor_factory = p_processor_factory

        if p_pusher_factory is None:
            self.pusher_factory = PrimalPusherFactory()
        else:
            self.pusher_factory = p_pusher_factory

        if p_database_module is None:
            self.database_module = DispatcherTicket._DEFAULT_DATABASE
        else:
            self.database_module = p_database_module

        if p_database_arguments is None:
            self.database_arguments = DispatcherTicket._DEFAULT_DATABASE_ARGS
        else:
            self.database_arguments = p_database_arguments

        if p_driver_module is None:
            self.driver_module = DispatcherTicket._DEFAULT_DRIVER
        else:
            self.driver_module = p_driver_module

        if p_external_config_files is None:
            self.external_config_files = []
        else:
            self.external_config_files = p_external_config_files

        if p_system_alias is None or p_system_alias == "":
            self.system_alias = "Databus"
        else:
            self.system_alias = p_system_alias

        self.dispatcher_observer = p_dispatcher_observer
        self.run_web_server = p_run_web_server
        self.web_server_port = p_web_server_port


class AbstractDispatcher(ABC): # pylint: disable=R0903
    """ Abstract dispatcher class """
    def __init__(self, p_ticket: DispatcherTicket = None):
        self.ticket = p_ticket
        self.external_config_file_manager = ExternalConfigFileManager()
        self.external_config_file_manager.add_files(self.ticket.external_config_files)

    @property
    def all_clients(self) -> List[Client]:
        """ Returns a list of clients from the database within the ticket """
        dummy_db = self.ticket.database_factory.create_database(
            p_log=Log(),
            p_module=self.ticket.database_module,
            p_client_id=None,
            p_passenger_factory=self.ticket.passenger_factory,
            p_arguments=self.ticket.database_arguments)

        return dummy_db.get_clients()

    @property
    @abstractmethod
    def dispatching(self) -> bool:
        """ Is the dispatcher active or not """

    @property
    @abstractmethod
    def paused(self) -> bool:
        """ Is the dispatcher paused or not """

    @property
    @abstractmethod
    def exporting(self) -> bool:
        """ Is export active or not """

    @property
    @abstractmethod
    def shutting_down(self) -> bool:
        """ Is shutdown active or not """

    @abstractmethod
    def expedite_client_passenger(self, p_client_id: str, p_passenger_module: str):
        """ Prioritizes the passenger in the next cycle """

    @abstractmethod
    def export_data_begin(self):
        """ Indicates that data export is starting """

    @abstractmethod
    def export_data_end(self):
        """ Indicates that data export is ending """

    def get_client_database(self, p_client_id: str, p_log: Log = None) -> AbstractDatabase:
        """ Returns a database instance for the given client """
        if p_log is None:
            log = Log()
        else:
            log = p_log

        return self.ticket.database_factory.create_database( # pylint: disable=C0103
            p_passenger_factory=self.ticket.passenger_factory,
            p_client_id=p_client_id,
            p_module=self.ticket.database_module,
            p_log=log,
            p_arguments=self.ticket.database_arguments)

    def get_driver(self) -> AbstractDriver:
        """ Returns a new driver instance """
        driver = self.ticket.driver_factory.create_driver(
            self.ticket.driver_module,
            self.ticket.queue_factory,
            self.ticket.processor_factory,
            self.ticket.puller_factory,
            self.ticket.pusher_factory)
        return driver

    @abstractmethod
    def start(self):
        """ Activates dispatcher timer """

    @abstractmethod
    def request_shutdown(self):
        """ Dispatcher shutdown """

    @abstractmethod
    def request_pause(self):
        """ Pauses dispatcher
        This is the antonym of resume
        """

    @abstractmethod
    def resume(self):
        """ Resumes the dispatcher
        This is the antonym of pause
        """

    def get_client_customizing_entry(self, p_client_id: str, p_entry_name: str) -> ClientCustomizing: # pylint: disable=C0301
        """ Returns a single node """
        all_entries = self.get_client_customizing_list(p_client_id=p_client_id)
        if all_entries is None or len(all_entries) < 0:
            return None
        for entry in all_entries[0].nodes:
            if entry.name == p_entry_name:
                return entry
        return None

    def get_client_customizing_list(self, p_client_id: str = None) -> List[ClientCustomizing]:
        """ Returns a list of client - customizing files """
        output = []

        for client in self.all_clients:
            if p_client_id is not None and client.id != p_client_id:
                continue
            client_nodes = []

            client_database = self.get_client_database(client.id)
            db_node = CustomizingNode(DATABUS_DB_NODE, client_database.customizing)
            client_nodes.append(db_node)

            if client.id == Client.ROOT:
                clients_node = CustomizingNode(CLIENTS_DB_NODE, client_database.client_master_data)
                client_nodes.append(clients_node)

            external_files = self.external_config_file_manager.get_files_of_client(client.id) # pylint: disable=C0301
            for external_file in external_files:
                external_node = CustomizingNode(external_file.file_id, external_file.file_content)
                client_nodes.append(external_node)

            output.append(ClientCustomizing(client, client_nodes))
        return output

    def backup_client_customizings(self):
        """ Backup client customizing"""
        customs = self.get_client_customizing_list()

        for custom in customs:
            db = self.get_client_database(custom.client.id)
            db.backup_client_customizing(p_cc=custom)
