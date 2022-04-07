""" Module to pull passenger from multiple Exchange accounts

If the expected E-Mails land to a single Exchange account, you can use
databus.puller.abstract_exchange.

If the expected E-Mail can land on multiple Exchange accounts, you can use
this module.
"""
from abc import ABC, abstractmethod
import json
from typing import List
from databus.client.log import Log
from databus.passenger.abstract_passenger import AbstractPassenger
from databus.passenger.attachment import Attachment
from databus.puller.abstract_puller import AbstractPuller
from databus.puller.abstract_exchange import AbstractExchange

class ExchangeAccount:
    """ Defines a singular Exchange account """
    def __init__(self, p_puller: AbstractExchange = None, p_alias: str = None):
        self.puller = p_puller
        self.alias = p_alias

class AbstractMultiExchange(AbstractPuller, ABC):
    """ Class to pull passenger from multiple Exchange accounts """
    _ARTIFICIAL_ATTACHMENT_FILE = "_databus_abstract_multi_exchange.json"

    def __init__(self, p_log: Log = None):
        super().__init__(p_log=p_log)

    @property
    @abstractmethod
    def exchange_accounts(self) -> List[ExchangeAccount]:
        """ Returns a list of Exchange accounts """

    def notify_passengers_seated(self, p_seated_passengers: List[AbstractPassenger]):
        """ Called after a passenger is properly queued.
        You would typically write a code here to ensure that the passenger is not
        returned any more when the puller works again.
        """
        for exchange_account in self.exchange_accounts:
            seated_passengers_of_account = []
            for seated_passenger in p_seated_passengers:
                artificial_attachment = seated_passenger.get_attachment_by_name(
                    AbstractMultiExchange._ARTIFICIAL_ATTACHMENT_FILE)
                aa_dict = json.loads(artificial_attachment.text_content)
                if aa_dict["alias"] == exchange_account.alias:
                    seated_passengers_of_account.append(seated_passenger)
            if len(seated_passengers_of_account) > 0:
                exchange_account.puller.notify_passengers_seated(seated_passengers_of_account)

    def pull(self) -> List[AbstractPassenger]:
        """ Pulls passengers from the source system """
        output = []
        for exchange_account in self.exchange_accounts:
            new_emails = exchange_account.puller.pull()
            for new_email in new_emails:
                artificial_attachment_dict = {"alias": exchange_account.alias}
                artificial_attachment_json = json.dumps(artificial_attachment_dict)
                artificial_attachment = Attachment(
                    p_name=AbstractMultiExchange._ARTIFICIAL_ATTACHMENT_FILE,
                    p_text_content=artificial_attachment_json)
                new_email.attachments.append(artificial_attachment)
                output.append(new_email)
        return output
