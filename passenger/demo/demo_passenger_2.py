from datetime import datetime
from passenger.abstract_passenger import AbstractPassenger
from passenger.attachment import Attachment
from uuid import UUID
from typing import List


class DemoPassenger2(AbstractPassenger):
    dataset: str

    def __init__(self,
                 p_external_id: str = "",
                 p_internal_id: UUID = None,
                 p_source_system: str = "",
                 p_attachments: List[Attachment] = [],
                 p_puller_module: str = "",
                 p_pull_datetime: datetime = datetime.now()):

        super().__init__(p_external_id=p_external_id,
                         p_internal_id=p_internal_id,
                         p_source_system=p_source_system,
                         p_attachments=p_attachments,
                         p_puller_module=p_puller_module,
                         p_pull_datetime=p_pull_datetime)
        self.dataset = "Demo dataset"

    def hello_world(self):
        print("Demo passenger 2 says hello world!")
        print("My dataset is: " + self.dataset)
