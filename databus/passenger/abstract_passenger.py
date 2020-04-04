""" Abstract passenger module """
from abc import ABC
from datetime import datetime
from typing import List
from uuid import uuid1, UUID
from databus.passenger.attachment import Attachment


class AbstractPassenger(ABC):
    """ Abstract passenger class """
    _clock_seq: int = 0

    def __init__(self,
                 p_external_id: str = None,
                 p_internal_id: UUID = None,
                 p_source_system: str = None,
                 p_attachments: List[Attachment] = None,
                 p_puller_module: str = None,
                 p_pull_datetime: datetime = None):

        if p_external_id is None:
            self.external_id = ""
        else:
            self.external_id = p_external_id

        if p_source_system is None:
            self.source_system = ""
        else:
            self.source_system = p_source_system

        if p_puller_module is None:
            self.puller_module = ""
        else:
            self.puller_module = p_puller_module

        if p_pull_datetime is None:
            self.pull_datetime = datetime.now()
        else:
            self.pull_datetime = p_pull_datetime

        if p_attachments is None:
            self.attachments = []
        else:
            self.attachments = p_attachments

        if p_internal_id is None:
            AbstractPassenger._clock_seq += 1
            self.internal_id = uuid1(clock_seq=AbstractPassenger._clock_seq)
        else:
            self.internal_id = p_internal_id

    @property
    def id_text(self) -> str:
        """ Returns the unique ID of the passenger as text """
        return self.source_system + " - " + self.external_id + " (" + str(self.internal_id) + ")"
