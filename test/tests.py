from client.client import Client
from client.log import Log, LogEntry
from config.constants import *
from database.abstract_database import AbstractDatabase
from database.factory import DatabaseFactory
from passenger.factory import PassengerFactory
from puller.abstract_puller import AbstractPuller
from puller.factory import PullerFactory


class DefaultTest:
    _demo_client: Client
    _demo_log: Log
    _demo_puller: AbstractPuller
    _db: AbstractDatabase

    def __init__(self):
        self._demo_client = Client()
        self._db = DatabaseFactory.get_instance()
        self._demo_log = Log()

    def run(self):
        # Start
        self._demo_log.entries.append(LogEntry("Test started"))

        # Master data
        self._read_passenger_types()
        # self._create_passenger()
        # self._read_puller_types()
        # self._create_puller()
        # self._pull()

        # Client
        self._read_clients()
        self._create_demo_client()
        self._client_pull()

        # Final
        self._demo_log.entries.append(LogEntry("Test finished"))
        self._save_log()

    def _client_pull(self):
        self._h1("Client is pulling")
        for puller in self._demo_client.pullers:
            print("Pulling with " + puller.__module__)
            pulled_passangers = puller.pull(p_log=self._demo_log)
            for pulled_passanger in pulled_passangers:
                print("Pulled passanger: " + pulled_passanger.dataset)

    def _create_demo_client(self):
        self._h1("Creating demo client")
        self._demo_client = self._db.get_client(DEMO_CLIENT)
        print("Sync frequency: " + str(self._demo_client.sync_frequency))
        print("Pullers of client:")
        for cp in self._demo_client.pullers:
            print(cp.__module__)

    def _create_passenger(self):
        self._h1("Creating passenger")
        demo_passenger = PassengerFactory.create_passenger(DEMO_PASSENGER_MODULE)
        print(demo_passenger)
        print("Module: " + demo_passenger.__module__)
        demo_passenger.hello_world()

    def _create_puller(self):
        self._h1("Creating puller")
        self._demo_puller = PullerFactory.create_puller(DEMO_PULLER_MODULE)
        print(self._demo_puller)
        print("Module: " + self._demo_puller.__module__)
        self._demo_puller.hello_world()

    def _h1(self, p_title: str):
        print("__________")
        print(p_title)

    def _pull(self):
        self._h1("Pulling passangers...")
        pulled_passangers = self._demo_puller.pull()
        for pulled_passanger in pulled_passangers:
            print("Pulled passanger: " + pulled_passanger.dataset)

    def _read_clients(self):
        self._h1("Reading all clients")
        all_clients = self._db.get_clients()
        for client in all_clients:
            print(client.name)

    def _read_passenger_types(self):
        self._h1("Reading passenger types")
        passenger_types = PassengerFactory.get_passenger_types()
        for pt in passenger_types:
            print(pt)

    def _read_puller_types(self):
        self._h1("Reading puller types")
        puller_types = PullerFactory.get_puller_types()
        for pt in puller_types:
            print(pt)

    def _save_log(self):
        self._h1("Saving log")
        self._db.insert_log(p_client=self._demo_client, p_log=self._demo_log)
