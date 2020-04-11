""" Demo passenger module """
from datetime import datetime
from uuid import UUID
from typing import List
from databus.passenger.abstract_passenger import AbstractPassenger
from databus.passenger.attachment import Attachment


class DemoPassenger1(AbstractPassenger):
    """ Demo passenger class """
    def __init__(self, # pylint: disable=R0913
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
        self.dataset = "Demo dataset"

    def hello_world(self):
        """ Dummy method """
        print("Demo passenger 1 says hello world!")
        print("My id is: " + str(self.internal_id))
        print("My dataset is: " + self.dataset)
