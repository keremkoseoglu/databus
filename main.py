""" Main entry point for Databus execution """
from os import path
import databus
from databus.client.external_config import ExternalConfigFile
from databus.database.sql_db.sql_database_arguments import SqlDatabaseArguments
from databus.dispatcher.abstract_dispatcher import DispatcherTicket
from databus.dispatcher.primal_factory import PrimalDispatcherFactory


def start_with_json_db():
    """ Starts instance using JSON DB """
    ticket = DispatcherTicket(p_system_alias="Databus DEV")
    PrimalDispatcherFactory().create_dispatcher(p_ticket=ticket).start()


def start_with_sql_db():
    """ Starts instance using SQL Server """
    sql_args = {
        SqlDatabaseArguments.KEY_DATABASE: "master",
        SqlDatabaseArguments.KEY_PASSWORD: "reallyStrongPwd123",
        SqlDatabaseArguments.KEY_SCHEMA: "databus",
        SqlDatabaseArguments.KEY_SERVER: "127.0.0.1,1433",
        SqlDatabaseArguments.KEY_USERNAME: "SA"
    }

    demo_config_path = path.join(databus.get_root_path(), "demo_external_config.json")
    demo_config_file = ExternalConfigFile("demo", "demo_config", demo_config_path)

    ticket = DispatcherTicket(
        p_database_module="databus.database.sql_db.sql_database",
        p_database_arguments=sql_args,
        p_external_config_files=[demo_config_file],
        p_system_alias="Development"
    )

    PrimalDispatcherFactory().create_dispatcher(p_ticket=ticket).start()


if __name__ == "__main__":
    start_with_json_db()
    #start_with_sql_db()
