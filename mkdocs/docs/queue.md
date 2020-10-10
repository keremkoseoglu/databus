# Queue

Just what it says. When you pull a new [passenger](passenger.md), it is stored in the queue until:

- The [puller](puller.md) system is notified 
- All [processors](processor.md) are complete
- The passenger is [pushed](pusher.md) to the target system

Therefore; the queue keeps track of the status of each [puller](puller.md), [processor](processor.md) and [pusher](pusher.md). It also keeps track of its corresponding log files, which can be viewed on the [web interface](web.md).

Even after everything is completed, the passenger lingers in the queue for a while. You can determine the wait time per [client](client.md). Check [database](database.md) section for queue configuration details. 

Databus comes with a default queue implementation: databus/pqueue/primal_queue.py . You'll want to use this most of the time. 

## Implementing a custom queue

Although highly improbable; if, for whatever reason, you need to implement your own queue class; here are the steps necessary.

- Derive a new class from databus.pqueue.abstract_queue
- Ensure that your .py file has only one class (which is the queue)
- Ensure calling super().__init__()
- Add the queue class to your client configuration. 
    - [json_db](database.md): /data/json_db/clients/(client name)/config.json
    - [sql_db](database.md): databus.passenger