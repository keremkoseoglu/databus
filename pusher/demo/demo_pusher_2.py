from client.log import Log, LogEntry
from passenger.abstract_passenger import AbstractPassenger
from pusher.abstract_pusher import AbstractPusher
from typing import List


class DemoPusher2(AbstractPusher):

    def push(self, p_log: Log, p_passengers: List[AbstractPassenger]):
        p_log.append("Pusher 2 did its job")

