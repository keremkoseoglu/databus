from abc import ABC, abstractmethod
from passenger.attachment import Attachment
from typing import List
from uuid import uuid1, UUID


class AbstractPassenger(ABC):
    attachments: List[Attachment]
    external_id: str
    internal_id: UUID
    source_system: str

    def __init__(self,
                 p_external_id: str = "",
                 p_internal_id: UUID = uuid1(),
                 p_source_system: str = "",
                 p_attachments: List[Attachment] = []):

        self.attachments = p_attachments
        self.external_id = p_external_id
        self.internal_id = p_internal_id
        self.source_system = p_source_system

    @property
    def id_text(self) -> str:
        return self.source_system + " - " + self.external_id + " (" + str(self.internal_id) + ")"