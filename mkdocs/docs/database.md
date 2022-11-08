# Database

Databus needs a database to store client and queue data. Out of the box, it supports:

- **json_db**: A custom written engine which stores the data on the disk as JSON files.
- **sql_db**: An engine to store data on a Microsoft SQL Server instance.

Both database engines have the same functionality. But naturally; SQL Server will be faster if you are dealing with large volumes of data.

Databus has the ability to export data. Check the export menu on the Web interface.

## JSON DB

JSON DB is a simple but robust solution to store queue data. It is based on storing data on the disk in JSON format. It is obviously not advisable for large volumes of data.

A typical JSON DB implementation will have the following structure:

- **/data/json_db/clients**: root directory
- **/data/json_db/clients/demo**: Demo client
- **/data/json_db/clients/demo/config.json**: Configuration of demo client
- **/data/json_db/clients/demo/log**: Log files (initially empty). For each new log, Databus will put a new .json file here.
- **/data/json_db/clients/demo/pqueue**: Queue files (initially empty). For each new queue entry, Databus will open a new folder here. 

For each new client you want to add, you can imitate the folder structure of the demo client.

config.json will have the following format:

```
{
    "log_life_span": 1,
    "passengers": [
        {
            "name": "databus.passenger.demo.demo_passenger_1",
            "processors": [
                "databus.processor.demo.demo_processor_1"
            ],
            "pullers": [
                "databus.puller.demo.demo_puller_1"
            ],
            "pushers": [
                "databus.pusher.demo.demo_pusher_1"
            ],
            "queue": "databus.pqueue.primal_queue",
            "queue_life_span": 1,
            "sync_frequency": 1
        }
    ],
    "users": [
        {
            "password": "demo",
            "role": "administrator",
            "token": "267c598e-f994-11ea-9005-acde48001122",
            "username": "demo"
        }
    ]
}
```

- **log_life_span**: For how many days should the log files live on the disk? They will be deleted afterwards. Backup preserve duration also depend on this setting.
- **passengers**: List of [passengers](passenger.md) of the client.
    - **name**: Name of the Python [passenger](passenger.md) module. This is our data to transport.
    - **pullers**: Names of Python [puller](puller.md) modules. Those are our data sources.
    - **processors**: Names of Python [processor](processor.md) modules. Those are the code files doing filtering, validation, etc.
    - **pushers**: Names of Python [pusher](pusher.md) modules. Those are our data targets.
    - **queue**: Name of the Python [queue](queue.md) module. Typically, you'll be using the primal queue.
    - **queue_life_span**: For how many days should the completed queue files live on the disk? They will be deleted afterwards.
    - **sync_frequency**: How often (in minutes) should Databus sync this passenger?
- **users**: List of Databus users of this client. Sub-fields are intuitive. 
    - **username**: Obvious
    - **password**: Obvious
    - **role**: Either "administrator" or "operator". Administrator has more capabilities on the [web](web.md) interface.

## SQL Server

Databus can run on a traditional SQL Server instance. To create a brand new set of Databus tables, you can use the file /databus/database/sql_db/creation_script.sql . After the database is created, you can start Databus with the appropriate dispatcher ticket to start against the database.

The tables are very intuitive. Following the explanation under JSON DB, just browse through the tables and you'll find your way around.

## Custom database

You can implement your own database engine too. All you need to do is to derive a new class from databus.database.abstract_database. Remember passing your own module name to the dispatcher as seen above.