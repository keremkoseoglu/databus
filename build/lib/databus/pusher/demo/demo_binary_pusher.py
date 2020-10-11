""" Demo binary pusher module """
from os import path
from databus.pqueue.queue_status import PassengerQueueStatus, QueueStatus
from databus.pusher.abstract_pusher import AbstractPusher


class DemoBinaryPusher(AbstractPusher): # pylint: disable=R0903
    """ Demo binary pusher class """
    _BIN_FILE_NAME = "sample_binary_file.png"
    _MODULE_FILE_NAME = "demo_binary_pusher.py"

    def push(self, p_passenger: PassengerQueueStatus):
        """ Push demonstration """
        self.log.append_text("Pushing passenger " + p_passenger.passenger.id_text)
        DemoBinaryPusher._write_binary_file(p_passenger.passenger.attachments[0].binary_content)
        p_passenger.set_pusher_status(self.__module__, QueueStatus.complete)

    @staticmethod
    def _write_binary_file(p_bin: bytearray):
        """ Writes binary file to disk """
        full_path = path.abspath(__file__).replace(DemoBinaryPusher._MODULE_FILE_NAME,
                                                   DemoBinaryPusher._BIN_FILE_NAME)
        with open(full_path, "wb") as bin_file:
            bin_file.write(p_bin)
