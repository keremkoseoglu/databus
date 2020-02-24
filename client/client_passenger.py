from typing import List


class ClientPassenger:
    def __init__(self,
                 p_name: str = "Undefined",
                 p_puller_modules: List[str] = [],
                 p_queue_module: str = "",
                 p_processor_modules: List[str] = [],
                 p_pusher_modules: List[str] = [],
                 p_sync_frequency: int = 0):

        self.name = p_name
        self.puller_modules = p_puller_modules
        self.queue_module = p_queue_module
        self.processor_modules = p_processor_modules
        self.pusher_modules = p_pusher_modules
        self.sync_frequency = p_sync_frequency

