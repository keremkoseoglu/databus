""" Abstract module to pull E-Mails from Exchange Server

If the expected E-Mails land to a single Exchange account, you can use
this module.

If the expected E-Mail can land on multiple Exchange accounts, you can use
databus.puller.abstract_multi_exchange .
"""
from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime
from typing import List
from uuid import uuid1
from exchangelib import DELEGATE, Account, Configuration, Credentials, Mailbox, Message
from databus.client.log import Log, LogEntry, MessageType
from databus.passenger.abstract_passenger import AbstractPassenger
from databus.passenger.attachment import Attachment, AttachmentFormat
from databus.passenger.email import Email
from databus.puller.abstract_puller import AbstractPuller


class ExchangeSettings: # pylint: disable=R0903
    """ Parameters to connect to Exchange Server """
    def __init__(self,
                 p_email: str = None,
                 p_username: str = None,
                 p_password: str = None,
                 p_server: str = None):
        if p_email is None:
            self.email = ""
        else:
            self.email = p_email

        if p_username is None:
            self.username = ""
        else:
            self.username = p_username

        if p_password is None:
            self.password = ""
        else:
            self.password = p_password

        if p_server is None:
            self.server = ""
        else:
            self.server = p_server


class AbstractExchange(AbstractPuller, ABC):
    """ Abstract class to pull E-Mails from Exchange Server """
    _SOURCE_SYSTEM = "Exchange"
    _DEFAULT_EMAIL_MODULE = "databus.passenger.email"

    def __init__(self, p_log: Log = None, p_alias: str = ""):
        super().__init__(p_log)
        self._settings = self.settings
        self._email_decorator = None
        self.account = AbstractExchange._login(self._settings)
        self.email_module = AbstractExchange._DEFAULT_EMAIL_MODULE
        self.alias = p_alias

        self.log.append_text(
            "Exchange user: " +
            self._settings.username +
            " - " +
            self._settings.email)

    @abstractproperty
    def settings(self) -> ExchangeSettings:
        """ Returns parameters to connect to Exchange server """

    def delete_seated_passengers_from_inbox(self, p_seated_passengers: List[AbstractPassenger]):
        """ Deletes seated passengers from the Exchange inbox
        This method is expected to be called from notify_passengers_seated in your concrete class.
        """
        for seated_passenger in p_seated_passengers:
            log_txt = "Attempting to delete mail from inbox: " + seated_passenger.id_text
            self.log.append_text(log_txt)
            found_in_inbox = False
            for inbox_item in self.account.inbox.all().order_by('-datetime_received'): # pylint: disable=E1101
                if seated_passenger.external_id == inbox_item.message_id:
                    found_in_inbox = True
                    inbox_item.soft_delete()
                    self.log.append_text("Deleted!")
                    break
            if not found_in_inbox:
                self.log.append_entry(LogEntry(p_message="Item not found in inbox, assuming manual deletion", p_type=MessageType.warning)) # pylint: disable=C0301

    @abstractmethod
    def notify_passengers_seated(self, p_seated_passengers: List[AbstractPassenger]):
        """ This method is called whenever the E-Mail from Exchange is properly queued.
        You can delete the E-Mail from Exchange Inbox here, or maybe move it to
        another folder?
        """

    def _pull(self) -> List[AbstractPassenger]:
        output = []

        for item in self.account.inbox.all().order_by('-datetime_received'):  # pylint: disable=E1101
            email_passenger = Email(p_external_id=item.message_id,
                                    p_internal_id=uuid1(),
                                    p_source_system=AbstractExchange._SOURCE_SYSTEM,
                                    p_attachments=[],
                                    p_puller_module=self.__module__,
                                    p_pull_datetime=datetime.now(),
                                    p_passenger_module=self.email_module)

            for item_attachment in item.attachments:
                try:
                    dummy = item_attachment.name
                    dummy = item_attachment.content
                except Exception: # pylint: disable=W0703
                    continue

                if any([item_attachment.name is None,
                        item_attachment.content is None]):
                    continue

                if any([item_attachment.content_type is None,
                        item_attachment.content_type == ""]):
                    attachment_format = Attachment.guess_format_by_file_name(
                        item_attachment.name)
                else:
                    attachment_format = Attachment.guess_format_by_mime_type(
                        item_attachment.content_type)

                if attachment_format == AttachmentFormat.text:
                    passenger_attachment = Attachment(
                        p_name=item_attachment.name,
                        p_format=AttachmentFormat.text,
                        p_text_content=str(item_attachment.content)[2:])
                else:
                    passenger_attachment = Attachment(
                        p_name=item_attachment.name,
                        p_format=AttachmentFormat.binary,
                        p_binary_content=item_attachment.content)

                email_passenger.attachments.append(passenger_attachment)

            if self._email_decorator is not None:
                self._email_decorator(item, email_passenger)
            self.log.append_text("Got mail from Exchange: " + email_passenger.id_text)
            output.append(email_passenger)

        return output

    def pull(self) -> List[AbstractPassenger]:
        """ Reads E-Mails from the given Exchange Server account """
        self._email_decorator = None
        return self._pull()

    def pull_with_email_decorator(self, p_decorator) -> List[AbstractPassenger]:
        """ Pulls E-Mails, calling p_decorator() to modify
        received email objects. p_decorator takes two parameters:
        1) Exchange item
        2) databus.passenger.email.Email
        """
        self._email_decorator = p_decorator
        output = self._pull()
        self._email_decorator = None
        return output

    def send_email(self, to: [str], subject: str, body: str): # pylint: disable=C0103
        """ Sends an E-Mail via Exchange Server """
        to_recipients = []
        for recipient in to:
            to_recipients.append(Mailbox(email_address=recipient))

        email_message = Message(account=self.account,
                                folder=self.account.sent,
                                subject=subject,
                                body=body,
                                to_recipients=to_recipients)

        email_message.send_and_save()

    @staticmethod
    def _login(settings: ExchangeSettings) -> Account:
        credentials = Credentials(username=settings.username,
                                  password=settings.password)

        if settings.server == "":
            account = Account(primary_smtp_address=settings.email,
                              credentials=credentials,
                              autodiscover=True,
                              access_type=DELEGATE)
        else:
            config = Configuration(server=settings.server, credentials=credentials)

            account = Account(primary_smtp_address=settings.email,
                              credentials=credentials,
                              autodiscover=False,
                              config=config,
                              access_type=DELEGATE)

        return account
