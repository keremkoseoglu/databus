from client.client import Client
from client.log import Log, LogEntry
from config.constants import *
from database.json_database import JsonDatabase


class DefaultTest:
    _demo_client: Client
    _json_db: JsonDatabase

    def __init__(self):
        self._demo_client = Client()
        self._json_db = JsonDatabase()

    def run(self):
        self._read_clients()
        self._create_demo_client()
        self._create_log()

    def _create_demo_client(self):
        print("Creating demo client")
        self._demo_client = Client(DEMO_CLIENT)

    def _create_log(self):
        print("Creating log file")
        log = Log(p_client=self._demo_client)
        log.entries.append(LogEntry("Hello world!"))
        log.entries.append(LogEntry("Hello moon!"))
        self._json_db.insert_log(log)

    def _read_clients(self):
        print("Reading all clients")
        all_clients = self._json_db.get_clients()
        for client in all_clients:
            print(client.name)
