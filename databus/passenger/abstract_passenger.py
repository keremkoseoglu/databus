""" Abstract passenger module """
from abc import ABC
from datetime import datetime
from typing import List
from uuid import uuid1, UUID
from databus.passenger.attachment import Attachment
from databus.passenger.unzip import Unzipper
from databus.passenger.html_link_downloader import HtmlLinkDownloader

class AbstractPassenger(ABC): # pylint: disable=R0903, R0902
    """ Abstract passenger class """
    _clock_seq: int = 0

    def __init__(self, # pylint: disable=R0913, R0912
                 p_external_id: str = None,
                 p_internal_id: UUID = None,
                 p_source_system: str = None,
                 p_attachments: List[Attachment] = None,
                 p_puller_module: str = None,
                 p_pull_datetime: datetime = None,
                 p_passenger_module: str = None,
                 p_log_guids: List[UUID] = None):

        if p_external_id is None:
            self.external_id = ""
        else:
            self.external_id = p_external_id

        if p_source_system is None:
            self.source_system = ""
        else:
            self.source_system = p_source_system

        if p_puller_module is None:
            self.puller_module = ""
        else:
            self.puller_module = p_puller_module

        if p_pull_datetime is None:
            self.pull_datetime = datetime.now()
        else:
            self.pull_datetime = p_pull_datetime

        if p_attachments is None:
            self.attachments = []
        else:
            self.attachments = p_attachments

        if p_internal_id is None:
            AbstractPassenger._clock_seq += 1
            self.internal_id = uuid1(clock_seq=AbstractPassenger._clock_seq)
        else:
            self.internal_id = p_internal_id

        if p_passenger_module is None:
            self.passenger_module = self.__module__
        else:
            self.passenger_module = p_passenger_module

        if p_log_guids is None:
            self._log_guids = []
        else:
            self._log_guids = p_log_guids

    @property
    def id_text(self) -> str:
        """ Returns the unique ID of the passenger as text """
        return self.source_system + " - " + self.external_id + " (" + str(self.internal_id) + ")"

    @property
    def log_guids(self) -> List[UUID]:
        """ Returns log guids """
        return self._log_guids

    def collect_log_guid(self, guid: UUID):
        """ Appends a new log guid, preventing duplicates """
        if guid in self._log_guids:
            return
        self._log_guids.append(guid)

    def get_attachment_by_name(self, name: str) -> Attachment:
        """ Returns the attachment """
        for attachment in self.attachments:
            if attachment.name == name:
                return attachment
        return None

    def unzip_attachments(self, p_extensions: List[str] = None):
        """ Finds .ZIP attachments, and turns them into regular
        attachments within the same object
        """
        Unzipper().execute(self.attachments, p_extensions)

    def download_links_in_html_as_attachments(self, p_html: str, p_extensions: List[str]):
        """ Scans the given HTML file, finds links, downloads
        the files and saves them as attachments.
        This method supports only text attachments at this time.
        """
        HtmlLinkDownloader().execute(self.attachments, p_html, p_extensions)
