from client.client import Client
from client.log import Log, LogEntry
from config.constants import *
from database.abstract_database import AbstractDatabase
from database.factory import DatabaseFactory
from passenger.factory import PassengerFactory


class DefaultTest:
    _demo_client: Client
    _db: AbstractDatabase

    def __init__(self):
        self._demo_client = Client()
        self._db = DatabaseFactory.get_instance()

    def run(self):
        self._read_clients()
        self._create_demo_client()
        self._create_log()
        self._read_passenger_types()
        self._create_passenger()

    def _create_demo_client(self):
        self._h1("Creating demo client")
        self._demo_client = Client(DEMO_CLIENT)
        print("Passengers of client:")
        for cp in self._demo_client.passengers:
            print(cp.module + ", frequency: " + str(cp.sync_frequency))

    def _create_log(self):
        self._h1("Creating log file")
        log = Log(p_client=self._demo_client)
        log.entries.append(LogEntry("Hello world!"))
        log.entries.append(LogEntry("Hello moon!"))
        self._db.insert_log(log)

    def _create_passenger(self):
        self._h1("Creating passenger")
        demo_passenger = PassengerFactory.create_passenger(DEMO_PASSENGER_MODULE)
        print(demo_passenger)
        print("Module: " + demo_passenger.__module__)
        demo_passenger.hello_world()

    def _h1(self, p_title: str):
        print("__________")
        print(p_title)

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
