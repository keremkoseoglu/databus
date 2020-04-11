""" Excel attachment filter module """
from typing import List
from databus.passenger.email import Email
from databus.pqueue.queue_status import PassengerQueueStatus, QueueStatus
from databus.processor.abstract_processor import AbstractProcessor


class EmailFilterExcelAttachment(AbstractProcessor): # pylint: disable=R0903
    """ Excel attachment filter class """

    def process(self, p_passengers: List[PassengerQueueStatus]):
        """ Marks E-Mails without Excel attachments as complete """
        self.log.append_text("Filtering E-Mails by Excel attachment")

        for pqs in p_passengers:
            email = pqs.passenger
            if EmailFilterExcelAttachment._has_excel_attachment(email):
                self.log.append_text(email.id_text + " has an Excel attachment")
                pqs.set_processor_status(self.__module__, QueueStatus.complete)
            else:
                self.log.append_text((email.id_text + " doesn't have Excel attachments"))
                pqs.set_all_processor_statuses(QueueStatus.complete)
                pqs.set_all_pusher_statuses(QueueStatus.complete)

    @staticmethod
    def _has_excel_attachment(received_email: Email) -> bool:
        excel_attachments = received_email.excel_attachments
        if len(excel_attachments) <= 0:
            return False
        return True
