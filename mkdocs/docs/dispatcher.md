# Dispatcher

This is the main engine of Databus. It is responsible of scheduling & invoking [drivers](driver.md); which are responsible of actually transporting data between systems.

Typically, your main access point to databus is the dispatcher. When you start up the dispatcher, it means that Databus is up and running. Check [startup](startup.md) for alternative ways of starting Databus.

## Dispatcher ticket

To start the dispatcher, you might probably need to provide a dispatcher ticket from your app to Databus. If you don't, it will start with the default options; which might be good enough for many cases!

Structure of a dispatcher ticket can be seen in databus.dispatcher.abstract_dispatcher.DispatcherTicket .

Parameters that should be left empty for the default values in most cases:

- **p_database_factory**: Name of the [database](database.md) factory module
- **p_driver_factory**: Name of the [driver](driver.md) factory module
- **p_passenger_factory**: Name of the [passenger](passenger.md) factory module
- **p_queue_factory**: Name of the [queue](queue.md) factory module
- **p_puller_factory**: Name of the [puller](puller.md) factory module
- **p_processor_factory**: Name of the [processor](processor.md) factory module
- **p_pusher_factory**: Name of the [pusher](pusher.md) factory module
- **p_driver_module**: Name of the [driver](driver.md) module

Parameters which are advised to be filled are:

- **p_database_module**: [Database](database.md) engine module to be used. The default engine is [JSON DB](database.md); however, you can use any supplied or custom-developed database engine here. 
- **p_database_arguments**: Arguments of the provided database module. [JSON DB](database.md) doesn't need any arguments, [SQL Server](database.md) needs some arguments, and your custom-developed database might need some arguments.
- **p_dispatcher_observer**: If you have implemented a custom observer class (explained above), you can pass your observer object here.
- **p_run_web_server**: Obvious
- **p_web_server_port**: Obvious
- **p_external_config_files**: If you have additional local JSON configuration files, you can pass their paths here so they become editable through the [web interface](web.md).
- **p_system_alias**: This value is displayed on top of the [web interface](web.md). Useful to distinguish test - live systems.

Inspect databus.dispatcher.abstract_dispatcher for further startup options which might have been missed in the documentation.

## Observer

"Observer" is a useful [design pattern](https://www.amazon.com/ABAP-Design-Patterns-Objects-PRESS/dp/1493214640); which also took a place within the dispatcher.

If your app needs to be aware of significant events within the dispatcher, you can write a custom class implementing databus.dispatcher.observer.DispatcherObserver, and pass the observer object to the dispatcher ticket (as explained below).

Check databus/dispatcher/observer.py for a list of events you can be listening to.
