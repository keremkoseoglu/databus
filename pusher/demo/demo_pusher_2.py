from client.log import Log
from pqueue.queue_status import PassengerQueueStatus, QueueStatus
from pusher.abstract_pusher import AbstractPusher


class DemoPusher2(AbstractPusher):

    def push(self, p_log: Log, p_passenger: PassengerQueueStatus):
        p_log.append_text("Pushed passenger " + p_passenger.passenger.id_text)
        p_passenger.set_pusher_status(self.__module__, QueueStatus.complete)

