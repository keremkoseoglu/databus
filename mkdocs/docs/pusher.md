# Pusher 

Pusher classes are defined to send passengers to target systems. For each target system, you may implement your own pusher class. 

You can find some demo implementations under databus/pusher/demo, or check "[Used by](index.md)" to see real life examples.

## Implementing a new pusher

To implement a new pusher;

- Ensure that the corresponding [passenger](passenger.md) & [puller](puller.md) classes exist. If not, create them first.
- Derive a new class from databus.pusher.abstract_pusher
- Ensure that your .py file has only one class (which is the pusher)
- Ensure calling super().__init__()
- Add the pusher class to your client configuration. 
    - [json_db](database.md): /data/json_db/clients/(client name)/config.json
    - [sql_db](database.md): databus.processor