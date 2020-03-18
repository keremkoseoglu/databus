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
                 p_message: str = None,
                 p_timestamp: datetime = datetime.now(),
                 p_type: MessageType = MessageType.info,
                 p_source: str = None):
        self._message = p_message
        self._timestamp = p_timestamp
        self._type = p_type

        if p_message is None:
            self._message = ""
        else:
            self._message = p_message

        if p_source == "" or p_source is None:
            frm = inspect.stack()[1]
            mod = inspect.getmodule(frm[0])
            self.source = mod.__name__
        else:
            self.source = p_source

    @property
    def message(self) -> str:
        return self._message

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def type(self) -> MessageType:
        return self._type


class Log:
    def __init__(self):
        self._creation_datetime = datetime.now()
        self._guid = uuid1()
        self._entries = []

    @property
    def creation_datetime(self) -> datetime:
        return self._creation_datetime

    @property
    def entries(self) -> List[LogEntry]:
        return self._entries

    @property
    def guid(self) -> UUID:
        return self._guid

    def append_entry(self, p_entry: LogEntry):
        if p_entry.source == "" or p_entry.source is None:
            frm = inspect.stack()[1]
            mod = inspect.getmodule(frm[0])
            p_entry.source = mod.__name__
        self._entries.append(p_entry)

    def append_text(self, p_entry: str, p_source: str = None):
        if p_source == "" or p_source is None:
            frm = inspect.stack()[1]
            mod = inspect.getmodule(frm[0])
            source = mod.__name__
        else:
            source = p_source
        self._entries.append(LogEntry(p_message=p_entry, p_source=source))


