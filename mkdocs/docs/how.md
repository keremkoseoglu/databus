# How it works

## A simple flow

Once Databus is up and running, here is what it does:

![Overview](img/flow.png?raw=true "Overview)

- [Passengers](passenger.md); such as E-Mails or customer orders, are stored in the source system(s).
- [Puller(s)](puller.md) detect & read new passengers periodically.
- [Queue](queue.md) stores those passengers in the [database](database.md).
- [Processors](processor.md) runs any required operations on the passengers; such as filtering, data conversion, etc.
- [Pusher(s)](pusher.md) transport the passenger to the target system(s).

## Significant features

- A simple [web interface](web)
- Supports any number of distinct [clients](client.md) with different configurations
- Each client can transport any number of [passengers](passenger.md)
- Different [passengers](passenger.md) can have different [sync schedules](dispatcher.md)
- In case of an error, Databus will [retry the operation](queue.md)
- You can pause / resume Databus if needed