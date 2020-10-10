# Passenger

Passenger defines a data type to travel between systems. If you are pulling E-Mails and forwarding them to your target system, E-Mail is your passenger.

General structure of a passenger can be seen under /databus/passenger/abstract_passenger.py . Each passenger implementation has to be a class derived from that.

You can find some demo implementations under databus/passenger/demo, or check "[Used by](index.md)" to see real life examples.

## Properties

A passenger will have the following properties:

- **external_id**: The unique ID given by the source system.
- **internal_id**: A unique ID given by Databus.
- **source_system**: Name of the system from which the passenger has been pulled.
- **attachments**: A list of attachments (see below for details).
- **puller_module**: Name of the Python module which pulled the passenger.
- **pull_datetime**: The date + time on which the passenger was pulled.
- **log_guids**: List of log ID's linked to this passenger

## Attachments

Except the properties mentioned above, any data that needs to be stored with the passenger can be added as an attachment. Databus supports text and binary attachments.

For example; if you got an E-Mail message, each attachment can obviously be added as a passenger attachment. But if you need to store the mail body as well, you can add it as an artificial attachment called _body.html . 

Or, if you need to store additional properties with the passenger, create an artificial attachment called _props.json and store it as an attachment.

Each attachment of a given passenger must have a unique name.

## Supplied passengers

Currently, Databus provides a passenger class for E-Mail messages under databus/passenger/email.py . If you need to pull E-Mails from a mail server, you can use this passenger. Hint: It also has an [Exchange Server puller](puller.md) to help you with that.

## Implementing a new passenger

- Create a new class derived from databus.passenger.abstract_passenger
- Ensure that your .py file has only one class (which is the passenger)
- Ensure calling super().__init__()
- You may need to implement corresponding puller / processor / pusher classes as well
- Add the puller class to your client configuration
    - [json_db](database.md): /data/json_db/clients/(client name)/config.json
    - [sql_db](database.md): databus.passenger