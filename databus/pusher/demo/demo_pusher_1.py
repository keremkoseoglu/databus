""" Demo pusher module """
from databus.pqueue.queue_status import PassengerQueueStatus, QueueStatus
from databus.pusher.abstract_pusher import AbstractPusher


class DemoPusher1(AbstractPusher): # pylint: disable=R0903
    """ Demo pusher class """
    def push(self, p_passenger: PassengerQueueStatus):
        """ Push demonstration """
        self.log.append_text(f"Pushed passenger {p_passenger.passenger.id_text}")
        p_passenger.set_pusher_status(self.__module__, QueueStatus.complete)
