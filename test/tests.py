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

    @staticmethod
    def run():
        # Factories
        database_factory = PrimalDatabaseFactory()
        driver_factory = PrimalDriverFactory()
        passenger_factory = PrimalPassengerFactory()
        processor_factory = PrimalProcessorFactory()
        puller_factory = PrimalPullerFactory()
        pusher_factory = PrimalPusherFactory()
        queue_factory = PrimalQueueFactory()

        # Objects
        driver = driver_factory.create_driver(DEMO_DRIVER,
                                              queue_factory,
                                              processor_factory,
                                              puller_factory,
                                              pusher_factory)
        log = Log()
        db = database_factory.create_database(DATABASE_MODULE, DEMO_CLIENT, log, passenger_factory)

        # Operation
        db.erase_passsenger_queue()

        for client_passenger in db.client.passengers:
            _ticket = BusTicket(p_client_passenger=client_passenger,
                                p_log=log,
                                p_database=db)
            driver.drive(_ticket)

        db.insert_log(log)

