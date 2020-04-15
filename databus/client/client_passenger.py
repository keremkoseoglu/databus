""" Client passenger module """
from datetime import datetime, timedelta
from typing import List


class ClientPassenger:  # pylint: disable=R0903
    """ Client passenger class """
    def __init__(self, # pylint: disable=R0913
                 p_name: str = "Undefined",
                 p_puller_modules: List[str] = None,
                 p_queue_module: str = None,
                 p_processor_modules: List[str] = None,
                 p_pusher_modules: List[str] = None,
                 p_sync_frequency: int = 0,
                 p_queue_life_span: int = 0):

        self.name = p_name
        self.sync_frequency = p_sync_frequency
        self.queue_life_span = p_queue_life_span

        if p_queue_module is None:
            self.queue_module = ""
        else:
            self.queue_module = p_queue_module

        if p_puller_modules is None:
            self.puller_modules = []
        else:
            self.puller_modules = p_puller_modules

        if p_processor_modules is None:
            self.processor_modules = []
        else:
            self.processor_modules = p_processor_modules

        if p_pusher_modules is None:
            self.pusher_modules = []
        else:
            self.pusher_modules = p_pusher_modules

    @property
    def queue_expiry_date(self) -> datetime:
        """ Returns queue expiry date """
        output = datetime.now() - timedelta(days=self.queue_life_span)
        return output
