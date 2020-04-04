from datetime import datetime
import os
from typing import List
from uuid import UUID

from databus.passenger.abstract_passenger import AbstractPassenger
from databus.passenger.attachment import Attachment, AttachmentFormat


class Email(AbstractPassenger):
    _EXCEL_EXTENSIONS = [".xls", ".xlsx"]

    def __init__(self,
                 p_external_id: str = None,
                 p_internal_id: UUID = None,
                 p_source_system: str = None,
                 p_attachments: List[Attachment] = None,
                 p_puller_module: str = None,
                 p_pull_datetime: datetime = None):
        super().__init__(p_external_id=p_external_id,
                         p_internal_id=p_internal_id,
                         p_source_system=p_source_system,
                         p_attachments=p_attachments,
                         p_puller_module=p_puller_module,
                         p_pull_datetime=p_pull_datetime)

    @property
    def excel_attachments(self) -> List[Attachment]:
        output = []
        for candidate in self.attachments:
            if "." not in candidate.name:
                continue
            file_name_parts = os.path.splitext(candidate.name)
            extension = file_name_parts[1].lower()
            if extension not in Email._EXCEL_EXTENSIONS:
                continue
            output.append(candidate)
        return output


