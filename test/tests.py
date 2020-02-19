from client.client import Client
from client.log import Log, LogEntry
from config.constants import *
from database.abstract_database import AbstractDatabase
from database.factory import DatabaseFactory
from passenger.abstract_passenger import AbstractPassenger
from passenger.factory import PassengerFactory
from pusher.factory import PusherFactory
from processor.factory import ProcessorFactory
from puller.abstract_puller import AbstractPuller
from puller.factory import PullerFactory
from pqueue.abstract_queue import AbstractQueue
from pqueue.factory import QueueFactory
from typing import List


class DefaultTest:
    _demo_log: Log
    _demo_passengers: List[AbstractPassenger]
    _demo_puller: AbstractPuller
    _db: AbstractDatabase

    def __init__(self):
        self._db = DatabaseFactory.create_database(DATABASE_MODULE, DEMO_CLIENT)
        self._demo_log = Log()
        self._demo_passengers = []
        self._demo_puller = None

    def run(self):
        # Start
        self._demo_log.append("Test started")

        # Master data
        # self._create_passenger()
        # self._read_puller_types()
        # self._pull()

        # Client
        self._read_clients()
        self._create_demo_client()
        self._client_pull()
        self._client_write_queue()
        self._client_process()
        self._client_push()

        # Final
        self._demo_log.append("Test finished")
        self._save_log()

    def _client_process(self):
        self._h1("Client is processing")
        for client_passenger in self._demo_client.passengers:
            print("- Processing passenger type " + client_passenger.name)
            for processor in client_passenger.processor_modules:
                print("-- Processing with " + processor)
                processor_obj = ProcessorFactory.create_processor(processor)
                processor_obj.process(p_log=self._demo_log, p_passengers=self._demo_passengers)

    def _client_pull(self):
        self._h1("Client is pulling")
        for client_passenger in self._demo_client.passengers:
            print("Pulling passenger type " + client_passenger.name)
            for puller in client_passenger.puller_modules:
                print("Pulling with " + puller)
                puller_obj = PullerFactory.create_puller(puller)
                pulled_passengers = puller_obj.pull(p_log=self._demo_log)
                for pulled_passenger in pulled_passengers:
                    print("Pulled passenger: " + pulled_passenger.external_id)
                    self._demo_passengers.append(pulled_passenger)

    def _client_push(self):
        self._h1("Client is pushing")
        for client_passenger in self._demo_client.passengers:
            print("Pushing passenger type " + client_passenger.name)
            queue = QueueFactory.create_queue(client_passenger.queue_module)

            undelivered_passengers = queue.get_undelivered_passengers(p_log=self._demo_log,
                                                                      p_client_id=self._demo_client.id,
                                                                      p_passenger_module=client_passenger.name,
                                                                      p_database=self._db)

            print("Got " + str(len(undelivered_passengers)) + " undelivered passengers")
            for pusher in client_passenger.pusher_modules:
                print("Pushing with " + pusher)
                pusher_obj = PusherFactory.create_pusher(pusher)
                pusher_obj.push(p_log=self._demo_log, p_passengers=undelivered_passengers)

            queue.set_passengers_delivered(p_client_id=self._demo_client.id,
                                           p_passengers=undelivered_passengers,
                                           p_log=self._demo_log,
                                           p_database=self._db)

    def _client_write_queue(self):
        self._h1("Writing pqueue")
        for passenger in self._demo_passengers:
            print("Writing " + passenger.external_id)
            client_passenger = self._demo_client.get_client_passenger(passenger.__module__)
            if client_passenger is None:
                # todo
                # yukarısı exception döndürmeli, burada try catch yap
                # return none yazan her yer de exception döndürmeli
                # burada log'da uyarı üretip devam et
                continue
            queue = QueueFactory.create_queue(client_passenger.queue_module)
            queue.insert(p_database=self._db,
                         p_client_id=self._demo_client.id,
                         p_passengers=[passenger],
                         p_log=self._demo_log)

    def _create_demo_client(self):
        self._h1("Creating demo client")
        self._demo_client = self._db.client
        print("Passengers of client:")
        for cp in self._demo_client.passengers:
            print(cp.name)
            print("- Pulls with:")
            for puller in cp.puller_modules:
                print("-- " + puller)
            print("- Processes with:")
            for processor in cp.processor_modules:
                print("-- " + processor)
            print("- Pushes with:")
            for pusher in cp.pusher_modules:
                print("-- " + pusher)

    def _create_passenger(self):
        self._h1("Creating passenger")
        demo_passenger = PassengerFactory.create_passenger(DEMO_PASSENGER_MODULE)
        print(demo_passenger)
        print("Module: " + demo_passenger.__module__)
        demo_passenger.hello_world()

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
            print(client.id)

    def _read_puller_types(self):
        self._h1("Reading puller types")
        puller_types = PullerFactory.get_puller_types()
        for pt in puller_types:
            print(pt)

    def _save_log(self):
        self._h1("Saving log")
        self._db.insert_log(p_log=self._demo_log)
