""" Main entry point for Databus execution """
from databus.dispatcher.abstract_dispatcher import DispatcherTicket
from databus.dispatcher.primal_factory import PrimalDispatcherFactory
from databus.database.sql_db.sql_database_arguments import SqlDatabaseArguments


def start_with_json_db():
    """ Starts instance using JSON DB """
    PrimalDispatcherFactory().create_dispatcher().start()


def start_with_sql_db():
    """ Starts instance using SQL Server """
    sql_args = {
        SqlDatabaseArguments.KEY_DATABASE: "Master",
        SqlDatabaseArguments.KEY_PASSWORD: "reallyStrongPwd123",
        SqlDatabaseArguments.KEY_SCHEMA: "databus",
        SqlDatabaseArguments.KEY_SERVER: "127.0.0.1,1433",
        SqlDatabaseArguments.KEY_USERNAME: "SA"
    }

    ticket = DispatcherTicket(
        p_database_module="databus.database.sql_db.sql_database",
        p_database_arguments=sql_args
    )

    PrimalDispatcherFactory().create_dispatcher(p_ticket=ticket).start()


if __name__ == "__main__":
    start_with_json_db()
