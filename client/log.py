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
    __message: str
    __timestamp: datetime
    __type: MessageType

    def __init__(self,
                 p_message: str = "",
                 p_timestamp: datetime = datetime.now(),
                 p_type: MessageType = MessageType.info):
        self.__message = p_message
        self.__timestamp = p_timestamp
        self.__type = p_type

    @property
    def message(self) -> str:
        return self.__message

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    @property
    def type(self) -> MessageType:
        return self.__type


class Log:
    __creation_datetime: datetime
    __entries: List[LogEntry]
    __guid: UUID

    def __init__(self):
        self.__creation_datetime = datetime.now()
        self.__guid = uuid1()
        self.__entries = []

    @property
    def creation_datetime(self) -> datetime:
        return self.__creation_datetime

    @property
    def entries(self) -> List[LogEntry]:
        return self.__entries

    @property
    def guid(self) -> UUID:
        return self.__guid

    def append(self, p_entry: LogEntry):
        self.__entries.append(p_entry)

    def append(self, p_entry: str):
        self.__entries.append(LogEntry(p_entry))
