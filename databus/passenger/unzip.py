""" Unzip module """
from typing import List
import mimetypes
import shutil
import os
from zipfile import ZipFile
from databus.passenger.attachment import Attachment, AttachmentFormat

class Unzipper:
    """ Main unzip class """
    _TMP_ZIP_DIR = "_tmp_zip"
    _TMP_ZIP_EXTRACT_DIR = "_extracted"
    _TMP_ZIP_FILE = "_tmp_zip.zip"

    def __init__(self):
        self._mime_type = mimetypes.MimeTypes()
        self._attachments = []
        self._deletable_indices = []
        self._new_attachments = []
        self._eligible_file_extensions = []
        self._extract_dir = os.path.join(Unzipper._TMP_ZIP_DIR, Unzipper._TMP_ZIP_EXTRACT_DIR)
        self._zip_path = os.path.join(Unzipper._TMP_ZIP_DIR, Unzipper._TMP_ZIP_FILE)

    def execute(self,
                p_attachments: List[Attachment],
                p_extensions: List[str] = None):
        """ Unzips attachments """
        self._attachments = p_attachments
        self._deletable_indices = []
        self._new_attachments = []

        if p_extensions is None:
            self._eligible_file_extensions = []
        else:
            self._eligible_file_extensions = p_extensions

        self._unzip()
        self._delete_zip_files()
        self._append_unzipped_files()

    def _download_zip_file(self, p_bin):
        shutil.rmtree(Unzipper._TMP_ZIP_DIR, ignore_errors=True)
        os.makedirs(Unzipper._TMP_ZIP_DIR, exist_ok=True)
        with open(self._zip_path, "wb") as zip_file:
            zip_file.write(p_bin)

    def _is_file_eligible(self, p_filename: str) -> bool:
        if p_filename is None or len(p_filename) <= 0:
            return False
        if len(self._eligible_file_extensions) <= 0:
            return True
        filename_len = len(p_filename)
        for efe in self._eligible_file_extensions:
            extension_len = len(efe)
            if filename_len <= (extension_len+1):
                continue
            filename_fragment = "." + p_filename[-extension_len:]
            supposed_extension = "." + efe
            if filename_fragment.lower() == supposed_extension.lower():
                return True

        return False

    def _extract_zip_file(self):
        extracted_files = []
        with ZipFile(self._zip_path) as zip_file:
            files_in_zip = zip_file.namelist()
            for file_in_zip in files_in_zip:
                if not self._is_file_eligible(file_in_zip):
                    continue
                extract_path = os.path.join(self._extract_dir, file_in_zip)
                zip_file.extract(file_in_zip, self._extract_dir)
                extracted_files.append(extract_path)

        for extracted_path in extracted_files:
            mime = self._mime_type.guess_type(extracted_path)[0]
            file_format = Attachment.guess_format_by_mime_type(mime)
            file_in_zip = os.path.split(extracted_path)[1]

            if file_format == AttachmentFormat.text:
                with open(extracted_path, "r", encoding="utf-8") as extracted_file:
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

            self._new_attachments.append(unzip_attachment)

    def _unzip(self):
        attachment_index = -1

        for attachment in self._attachments:
            attachment_index += 1
            if len(attachment.name) < 4:
                continue
            if attachment.name.upper()[-4:] != ".ZIP":
                continue

            self._download_zip_file(attachment.binary_content)
            self._extract_zip_file()
            self._deletable_indices.append(attachment_index)
            shutil.rmtree(Unzipper._TMP_ZIP_DIR, ignore_errors=True)

    def _delete_zip_files(self):
        self._deletable_indices.sort(reverse=True)
        for deletable_index in self._deletable_indices:
            self._attachments.pop(deletable_index)

    def _append_unzipped_files(self):
        for new_attachment in self._new_attachments:
            self._attachments.append(new_attachment)
