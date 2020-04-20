""" Main entry point for Databus execution """
from databus.dispatcher.abstract_dispatcher import DispatcherTicket
from databus.dispatcher.primal_factory import PrimalDispatcherFactory
from databus.client.log import Log
from databus.passenger.primal_factory import PrimalPassengerFactory
from databus.database.sql_db.sql_database import SqlDatabase
from databus.database.sql_db.sql_database_arguments import SqlDatabaseArguments

if __name__ == "__main__":
    # todo
    # sql server bitecek
    # burayı eski haline getir
    # PrimalDispatcherFactory().create_dispatcher().start()
    #test_connection()

    sql_args = {
        SqlDatabaseArguments.KEY_DATABASE: "databus_db",
        SqlDatabaseArguments.KEY_PASSWORD: "Honk+honk+2",
        SqlDatabaseArguments.KEY_SCHEMA: "databus",
        SqlDatabaseArguments.KEY_SERVER: "databus-server.database.windows.net",
        SqlDatabaseArguments.KEY_USERNAME: "databus"
    }

    # todo geçici kod
    
    ticket = DispatcherTicket(
        p_database_module="databus.database.sql_db.sql_database",
        p_database_arguments=sql_args
    )

    PrimalDispatcherFactory().create_dispatcher(p_ticket=ticket).start()

    
    """
    log = Log()
    passenger_factory = PrimalPassengerFactory()

    sql = SqlDatabase(
        p_arguments=sql_args,
        p_log=log,
        p_passenger_factory=passenger_factory,
        p_client_id="demo"
    )

    x = sql.get_log_list()

    clients = sql.get_clients()
    for client in clients:
        print(client.id)
        for passenger in client.passengers:
            print(passenger.name)
    """
    
