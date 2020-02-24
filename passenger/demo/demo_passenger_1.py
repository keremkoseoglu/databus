from passenger.abstract_passenger import AbstractPassenger
from uuid import uuid1, UUID


class DemoPassenger1(AbstractPassenger):
    dataset: str

    def __init__(self,
                 p_external_id: str = "",
                 p_internal_id: UUID = None,
                 p_source_system: str = "",
                 p_attachments: list = [],
                 p_puller_module: str = ""):

        super().__init__(p_external_id=p_external_id,
                         p_internal_id=p_internal_id,
                         p_source_system=p_source_system,
                         p_attachments=p_attachments,
                         p_puller_module=p_puller_module)
        self.dataset = "Demo dataset"

    def hello_world(self):
        print("Demo passenger 1 says hello world!")
        print("My id is: " + str(self.internal_id))
        print("My dataset is: " + self.dataset)
