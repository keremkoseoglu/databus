from enum import Enum


class QueueStatus(Enum):
    undefined = 0
    undelivered = 1
    delivered = 2
