from pqueue.queue_status import PassengerQueueStatus, QueueStatus
from pusher.abstract_pusher import AbstractPusher


class DemoPusher2(AbstractPusher):

    def push(self, p_passenger: PassengerQueueStatus):
        self.log.append_text("Pushed passenger " + p_passenger.passenger.id_text)
        p_passenger.set_pusher_status(self.__module__, QueueStatus.complete)

