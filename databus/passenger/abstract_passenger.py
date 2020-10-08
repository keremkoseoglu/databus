""" Abstract passenger module """
from abc import ABC
from datetime import datetime
from typing import List
from uuid import uuid1, UUID
from zipfile import ZipFile
import os
import shutil
import mimetypes
from urlextract import URLExtract
import requests
from databus.passenger.attachment import Attachment, AttachmentFormat


class AbstractPassenger(ABC): # pylint: disable=R0903, R0902
    """ Abstract passenger class """
    _clock_seq: int = 0
    _TMP_ZIP_DIR = "_tmp_zip"
    _TMP_ZIP_EXTRACT_DIR = "_extracted"
    _TMP_ZIP_FILE = "_tmp_zip.zip"

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

    def unzip_attachments(self):
        """ Finds .ZIP attachments, and turns them into regular
        attachments within the same object
        """
        mime_type = mimetypes.MimeTypes()
        attachment_index = -1
        deletable_indices = []
        new_attachments = []

        for attachment in self.attachments:
            attachment_index += 1
            if len(attachment.name) < 4:
                continue
            if attachment.name.upper()[-4:] != ".ZIP":
                continue

            shutil.rmtree(AbstractPassenger._TMP_ZIP_DIR, ignore_errors=True)
            os.makedirs(AbstractPassenger._TMP_ZIP_DIR, exist_ok=True)

            extract_dir = os.path.join(
                AbstractPassenger._TMP_ZIP_DIR,
                AbstractPassenger._TMP_ZIP_EXTRACT_DIR)

            zip_path = os.path.join(AbstractPassenger._TMP_ZIP_DIR, AbstractPassenger._TMP_ZIP_FILE)
            with open(zip_path, "wb") as zip_file:
                zip_file.write(attachment.binary_content)

            extracted_files = []
            with ZipFile(zip_path) as zip_file:
                files_in_zip = zip_file.namelist()
                for file_in_zip in files_in_zip:
                    extract_path = os.path.join(extract_dir, file_in_zip)
                    zip_file.extract(file_in_zip, extract_dir)
                    extracted_files.append(extract_path)

            for extracted_path in extracted_files:
                mime = mime_type.guess_type(extracted_path)[0]
                file_format = Attachment.guess_format_by_mime_type(mime)
                file_in_zip = os.path.split(extracted_path)[1]

                if file_format == AttachmentFormat.text:
                    with open(extracted_path, "r") as extracted_file:
                        file_content = extracted_file.read()
                        file_content = file_content.replace("\n", " ")
                        file_content = file_content.replace("\t", " ")
                    unzip_attachment = Attachment(
                        p_name=file_in_zip,
                        p_format=AttachmentFormat.text,
                        p_text_content=file_content)
                else:
                    with open(extracted_path, "rb") as extracted_file:
                        file_content = extracted_file.read()
                    unzip_attachment = Attachment(
                        p_name=file_in_zip,
                        p_format=AttachmentFormat.binary,
                        p_binary_content=file_content)

                new_attachments.append(unzip_attachment)

            deletable_indices.append(attachment_index)
            shutil.rmtree(AbstractPassenger._TMP_ZIP_DIR, ignore_errors=True)

        deletable_indices.sort(reverse=True)
        for deletable_index in deletable_indices:
            self.attachments.pop(deletable_index)

        for new_attachment in new_attachments:
            self.attachments.append(new_attachment)

    def download_links_in_html_as_attachments(self, p_html: str, p_extensions: List[str]):
        """ Scans the given HTML file, finds links, downloads
        the files and saves them as attachments.
        This method supports only text attachments at this time.
        """
        # Build clean HTML
        if p_html is None or len(p_html) <= 0:
            return
        clean_html = p_html.replace("\r", "").replace("\n", "")
        html_tag_pos = clean_html.lower().find("<html")
        if html_tag_pos < 0:
            return
        clean_html = clean_html[html_tag_pos:]

       # Extract URL's
        extractor = URLExtract()
        urls = extractor.find_urls(clean_html)

        # Download as necessary
        for url in urls:
            low_url = url.lower()
            has_eligible_extension = False
            for extension in p_extensions:
                low_extension = "." + extension.lower()
                if low_extension in low_url:
                    has_eligible_extension = True
                    break
            if not has_eligible_extension:
                continue

            if "urldefense.com" in url:
                real_http_pos = low_url.rfind("http")
                clean_url = url[real_http_pos:].replace("__", "")
            else:
                clean_url = url
            if clean_url[-1] == "/":
                clean_url = clean_url[:-1]

            filename = os.path.basename(clean_url)
            dummy_name, extension = os.path.splitext(filename)
            extension = extension.replace(".", "")
            file_format = Attachment.guess_format_by_file_extension(extension)

            response = requests.get(clean_url, allow_redirects=True)

            if file_format == AttachmentFormat.text:
                downloaded_attachment = Attachment(
                    p_name=filename,
                    p_format=AttachmentFormat.text,
                    p_text_content=response.text)
            else:
                downloaded_attachment = Attachment(
                    p_name=filename,
                    p_format=AttachmentFormat.binary,
                    p_binary_content=response.content)

            self.attachments.append(downloaded_attachment)
