""" Log module """
from datetime import datetime
from enum import Enum
import inspect
from typing import List
from uuid import uuid1, UUID


class MessageType(Enum):
    """ Message type """
    undefined = 0
    info = 1
    warning = 2
    error = 3


class LogEntry:
    """ Log entry class """
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
        """ Log entry as string """
        return self._message

    @property
    def timestamp(self) -> datetime:
        """ Log entry creation time """
        return self._timestamp

    @property
    def type(self) -> MessageType:
        """ Log entry message type """
        return self._type


class Log:
    """ Log class """
    def __init__(self):
        self._creation_datetime = datetime.now()
        self._guid = uuid1()
        self._entries = []

    @staticmethod
    def build_entry_field_string(p_date: str, p_source: str, p_type: str, p_message: str) -> str:
        """ Builds a string from entry fields """
        new_line = "[" + p_date + "]"
        new_line += "[" + p_source + "]"
        new_line += "[" + p_type + "]"
        new_line += " " + p_message
        return new_line

    @property
    def creation_datetime(self) -> datetime:
        """ Log creation time """
        return self._creation_datetime

    @property
    def entries(self) -> List[LogEntry]:
        """ All log entries """
        return self._entries

    @property
    def entries_as_string(self) -> str:
        """ Converts all log entries into string format """
        output = ""
        for entry in self.entries:
            new_line = Log.build_entry_field_string(
                entry.timestamp.isoformat(),
                entry.source,
                str(entry.type.name),
                entry.message)
            if output != "":
                output += "\r\n"
            output += new_line
        return output

    @property
    def guid(self) -> UUID:
        """ Unique log ID """
        return self._guid

    @property
    def has_error(self) -> bool:
        """ Returns true if there is any error message present """
        for entry in self._entries:
            if entry.type == MessageType.error:
                return True
        return False

    def append_entry(self, p_entry: LogEntry):
        """ Adds new entry to log """
        if p_entry.source == "" or p_entry.source is None:
            frm = inspect.stack()[1]
            mod = inspect.getmodule(frm[0])
            p_entry.source = mod.__name__
        self._entries.append(p_entry)

    def append_text(self, p_entry: str, p_source: str = None):
        """ Adds simple text to log """
        if p_source == "" or p_source is None:
            frm = inspect.stack()[1]
            mod = inspect.getmodule(frm[0])
            source = mod.__name__
        else:
            source = p_source
        self._entries.append(LogEntry(p_message=p_entry, p_source=source))
