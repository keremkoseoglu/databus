from datetime import datetime
from enum import Enum
import inspect
from typing import List
from uuid import uuid1, UUID


class MessageType(Enum):
    undefined = 0
    info = 1
    warning = 2
    error = 3


class LogEntry:
    def __init__(self,
                 p_message: str = "",
                 p_timestamp: datetime = datetime.now(),
                 p_type: MessageType = MessageType.info,
                 p_source: str = ""):
        self.__message = p_message
        self.__timestamp = p_timestamp
        self.__type = p_type

        if p_source == "" or p_source is None:
            frm = inspect.stack()[1]
            mod = inspect.getmodule(frm[0])
            self.source = mod.__name__
        else:
            self.source = p_source

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

    def append_entry(self, p_entry: LogEntry):
        if p_entry.source == "" or p_entry.source is None:
            frm = inspect.stack()[1]
            mod = inspect.getmodule(frm[0])
            p_entry.source = mod.__name__
        self.__entries.append(p_entry)

    def append_text(self, p_entry: str, p_source: str = ""):
        if p_source == "" or p_source is None:
            frm = inspect.stack()[1]
            mod = inspect.getmodule(frm[0])
            source = mod.__name__
        else:
            source = p_source
        self.__entries.append(LogEntry(p_message=p_entry,
                                       p_source=source))


