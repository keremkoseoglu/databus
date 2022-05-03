""" Module for value conversions """
from typing import Protocol
from databus.client.log import MessageType
from databus.passenger.attachment import AttachmentFormat
from databus.pqueue.queue_status import QueueStatus

class AbstractConverter(Protocol):
    """ Abstract converter class """
    @staticmethod
    def attachment_format(input_val):
        """ Attachment format conversion """

    @staticmethod
    def boolean(input_val):
        """ Boolean value conversion """

    @staticmethod
    def date_time(input_val):
        """ Date conversion """

    @staticmethod
    def message_type(input_val):
        """ Message type conversion """

    @staticmethod
    def queue_status(input_val):
        """ Queue status conversion """


class DatabusToSql(AbstractConverter):
    """ Databus - SQL conversion """
    @staticmethod
    def attachment_format(input_val):
        """ Attachment format conversion """
        if input_val == AttachmentFormat.binary:
            return "B"
        if input_val == AttachmentFormat.text:
            return "T"
        raise Exception("Unknown attachment format " + str(input_val))

    @staticmethod
    def boolean(input_val):
        """ Boolean value conversion """
        if input_val:
            return 1
        return 0

    @staticmethod
    def date_time(input_val):
        """ Date conversion """
        year = str(input_val.year)
        month = DatabusToSql._get_numc(str(input_val.month), 2)
        day = DatabusToSql._get_numc(str(input_val.day), 2)
        hour = DatabusToSql._get_numc(str(input_val.hour), 2)
        minute = DatabusToSql._get_numc(str(input_val.minute), 2)
        second = DatabusToSql._get_numc(str(input_val.second), 2)
        return year + month + day + " " + hour + ":" + minute + ":" + second + ".000"

    @staticmethod
    def message_type(input_val):
        """ Message type conversion """
        if input_val == MessageType.error:
            return "E"
        if input_val == MessageType.info:
            return "I"
        if input_val == MessageType.undefined:
            return "U"
        if input_val == MessageType.warning:
            return "W"
        raise Exception(f"Unknown message type {str(input_val)}")

    @staticmethod
    def queue_status(input_val):
        """ Queue status conversion """
        if input_val == QueueStatus.undefined:
            return "U"
        if input_val == QueueStatus.incomplete:
            return "I"
        if input_val == QueueStatus.complete:
            return "C"
        raise Exception("Unknown queue status " + str(input_val))

    @staticmethod
    def _get_numc(p_str: str, p_len: int) -> str:
        output = p_str
        while len(output) < p_len:
            output = "0" + output
        return output


class SqlToDatabus(AbstractConverter):
    """ SQL - Databus conversion """
    @staticmethod
    def attachment_format(input_val):
        """ Attachment format conversion """
        if input_val == "B":
            return AttachmentFormat.binary
        if input_val == "T":
            return AttachmentFormat.text
        raise Exception(f"Unknown attachment format {input_val}")

    @staticmethod
    def boolean(input_val):
        """ Boolean value conversion """
        return input_val == 1

    @staticmethod
    def date_time(input_val):
        """ Date conversion
        Current SQL driver returns native date time objects, so
        no conversion is needed.
        """
        return input_val

    @staticmethod
    def message_type(input_val):
        """ Message type conversion """
        if input_val == "E":
            return MessageType.error
        if input_val == "I":
            return MessageType.info
        if input_val == "U":
            return MessageType.undefined
        if input_val == "W":
            return MessageType.warning
        raise Exception("Unknown message type " + input_val)

    @staticmethod
    def queue_status(input_val):
        """ Queue status conversion """
        if input_val == "U":
            return QueueStatus.undefined
        if input_val == "I":
            return QueueStatus.incomplete
        if input_val == "C":
            return QueueStatus.complete
        raise Exception(f"Unknown queue status {str(input_val)}")
