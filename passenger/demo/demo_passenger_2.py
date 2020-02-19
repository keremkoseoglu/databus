from passenger.abstract_passenger import AbstractPassenger
from uuid import uuid1, UUID


class DemoPassenger2(AbstractPassenger):
    dataset: str

    def __init__(self,
                 p_external_id: str = "",
                 p_internal_id: UUID = uuid1(),
                 p_source_system: str = "",
                 p_attachments: list = []):

        super().__init__(p_external_id=p_external_id,
                         p_internal_id=p_internal_id,
                         p_source_system=p_source_system,
                         p_attachments=p_attachments)
        self.dataset = "Demo dataset"

    def hello_world(self):
        print("Demo passenger 2 says hello world!")
        print("My dataset is: " + self.dataset)
