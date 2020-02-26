from client.log import Log
from config.constants import *
from database.primal_factory import PrimalDatabaseFactory
from driver.abstract_driver import BusTicket
from driver.primal_factory import PrimalDriverFactory
from passenger.primal_factory import PrimalPassengerFactory
from pqueue.primal_factory import PrimalQueueFactory
from puller.primal_factory import PrimalPullerFactory
from pusher.primal_factory import PrimalPusherFactory
from processor.primal_factory import PrimalProcessorFactory


class DefaultTest:

    def __init__(self):
        # Factories
        self._database_factory = PrimalDatabaseFactory()
        self._driver_factory = PrimalDriverFactory()
        self._passenger_factory = PrimalPassengerFactory()
        self._processor_factory = PrimalProcessorFactory()
        self._puller_factory = PrimalPullerFactory()
        self._pusher_factory = PrimalPusherFactory()
        self._queue_factory = PrimalQueueFactory()

        # Objects
        self._driver = self._driver_factory.create_driver(
            DEMO_DRIVER,
            self._queue_factory,
            self._processor_factory,
            self._puller_factory,
            self._pusher_factory)

        log = Log()

        self._db = self._database_factory.create_database(
            DATABASE_DEFAULT,
            DEMO_CLIENT,
            log,
            self._passenger_factory)

    def erase_demo_client_queue(self):
        self._db.erase_passsenger_queue()

    def run(self):
        self.erase_demo_client_queue()
        log = Log()

        for client_passenger in self._db.client.passengers:
            _ticket = BusTicket(p_client_passenger=client_passenger,
                                p_log=log,
                                p_database=db)
            self._driver.drive(_ticket)

        self._db.insert_log(log)

