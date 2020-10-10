# Startup

Running a Databus instance is really easy! 

## Default configuration

```
from databus.dispatcher.primal_factory import PrimalDispatcherFactory
PrimalDispatcherFactory().create_dispatcher().start()
```

This will start Databus with the default configuration, which uses json_db. Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) to see what it's been doing.

The default demo account is demo:demo:demo. The default admin account is root:root:root. On a live system, you are advised to change this in your [database](database.md).

## Custom configuration

To start Databus with a custom configuration, you can provide a [dispatcher ticket](dispatcher.md). Here is an example.

```
from databus.database.sql_db.sql_database_arguments import SqlDatabaseArguments
from databus.dispatcher.abstract_dispatcher import DispatcherTicket
from databus.dispatcher.primal_factory import PrimalDispatcherFactory

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
```

Check the [dispatcher ticket](dispatcher.md) section for a complete list of parameters.
