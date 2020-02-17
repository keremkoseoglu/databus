from datetime import datetime
from enum import Enum
from typing import List
from uuid import uuid1, UUID


class MessageType(Enum):
    undefined = 0
    info = 1
    warning = 2
    error = 3


class LogEntry:
    message: str
    timestamp: datetime
    type: MessageType

    def __init__(self,
                 p_message: str = "",
                 p_timestamp: datetime = datetime.now(),
                 p_type: MessageType = MessageType.info):
        self.message = p_message
        self.timestamp = p_timestamp
        self.type = p_type


class Log:
    creation_datetime: datetime
    entries: List[LogEntry]
    guid: UUID

    def __init__(self):
        self.creation_datetime = datetime.now()
        self.guid = uuid1()
        self.entries = []
