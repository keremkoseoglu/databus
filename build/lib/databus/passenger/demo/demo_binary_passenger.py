""" Demo binary passenger module """
from datetime import datetime
from uuid import UUID
from typing import List
from databus.passenger.abstract_passenger import AbstractPassenger
from databus.passenger.attachment import Attachment


class DemoBinaryPassenger(AbstractPassenger): # pylint: disable=R0903
    """ Demo binary passenger class """
    def __init__(self, # pylint: disable=R0913
                 p_external_id: str = None,
                 p_internal_id: UUID = None,
                 p_source_system: str = None,
                 p_attachments: List[Attachment] = None,
                 p_puller_module: str = None,
                 p_pull_datetime: datetime = None,
                 p_passenger_module: str = None):

        if p_passenger_module is None:
            passenger_module = self.__module__
        else:
            passenger_module = p_passenger_module

        super().__init__(p_external_id=p_external_id,
                         p_internal_id=p_internal_id,
                         p_source_system=p_source_system,
                         p_attachments=p_attachments,
                         p_puller_module=p_puller_module,
                         p_pull_datetime=p_pull_datetime,
                         p_passenger_module=passenger_module)
