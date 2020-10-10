# Driver

Driver is the component responsible of running a data transfer operation.

Reminder: [Dispatcher](dispatcher.md) is responsible of scheduling drivers. When the time comes, driver is the component doing the actual work.

When the driver is executed; it will take the following steps; as seen in databus/driver/primal_driver.py:

- Pull new [passengers](passenger.md) from the source system
- Seat [passengers](passenger.md) into the [queue](queue.md)
- Notify the source system about seated passengers
- [Process](proecssor.md) seated passengers
- [Push](pusher.md) seated passengers to the target system

The [queue](queue.md) takes note of failures of each step. Driver will retry any failed step on the next schedule. However, users are able to manually alter statuses of each step through the [web](web.md) interface.
