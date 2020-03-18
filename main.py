from databus.database.primal_factory import PrimalDatabaseFactory
from databus.dispatcher.abstract_factory import DispatcherTicket
from databus.dispatcher.primal_factory import PrimalDispatcherFactory
from databus.driver.primal_factory import PrimalDriverFactory
from databus.passenger.primal_factory import PrimalPassengerFactory
from databus.pqueue.primal_factory import PrimalQueueFactory
from databus.puller.primal_factory import PrimalPullerFactory
from databus.pusher.primal_factory import PrimalPusherFactory
from databus.processor.primal_factory import PrimalProcessorFactory

_DEFAULT_DATABASE = "databus.database.json_db.json_database"
_DEFAULT_DRIVER = "databus.driver.primal_driver"
_DEFAULT_DISPATCHER = "databus.dispatcher.primal_dispatcher"

if __name__ == "__main__":

    _dispatcher_ticket = DispatcherTicket(
        p_database_factory=PrimalDatabaseFactory(),
        p_driver_factory=PrimalDriverFactory(),
        p_passenger_factory=PrimalPassengerFactory(),
        p_queue_factory=PrimalQueueFactory(),
        p_puller_factory=PrimalPullerFactory(),
        p_processor_factory=PrimalProcessorFactory(),
        p_pusher_factory=PrimalPusherFactory(),
        p_database_module=_DEFAULT_DATABASE,
        p_driver_module=_DEFAULT_DRIVER)

    PrimalDispatcherFactory().create_dispatcher(
        p_module=_DEFAULT_DISPATCHER,
        p_ticket=_dispatcher_ticket).start()




