from abc import ABC
from datetime import datetime
from passenger.attachment import Attachment
from typing import List
from uuid import uuid1, UUID


class AbstractPassenger(ABC):
    _clock_seq: int = 0

    def __init__(self,
                 p_external_id: str = "",
                 p_internal_id: UUID = None,
                 p_source_system: str = "",
                 p_attachments: List[Attachment] = [],
                 p_puller_module: str = "",
                 p_pull_datetime: datetime = datetime.now()):

        self.attachments = p_attachments
        self.external_id = p_external_id
        self.source_system = p_source_system
        self.puller_module = p_puller_module
        self.pull_datetime = p_pull_datetime

        if p_internal_id is None:
            AbstractPassenger._clock_seq += 1
            self.internal_id = uuid1(clock_seq=AbstractPassenger._clock_seq)
        else:
            self.internal_id = p_internal_id

    @property
    def id_text(self) -> str:
        return self.source_system + " - " + self.external_id + " (" + str(self.internal_id) + ")"
