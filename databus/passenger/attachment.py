""" Attachment module
All settings, data, files, etc of a passengers are
considered to be separate attachment files.
If you need to store some settings and definitions
per passenger, consider creating a JSON attachment.
"""
from enum import Enum
from typing import List
from os import path


class AttachmentError(Exception):
    """ Attachment exception class """

    class ErrorCode(Enum):
        """ Attachment error code """
        invalid_format: 1
        invalid_name: 2
        duplicate_name: 3

    def __init__(self, p_error_code: ErrorCode, p_format: str = None, p_name: str = None):
        super().__init__()
        self.error_code = p_error_code

        if p_format is None:
            self.format = ""
        else:
            self.format = p_format

        if p_name is None:
            self.name = ""
        else:
            self.name = p_name

    @property
    def message(self) -> str:
        """ Attachment error text """
        if self.ErrorCode == AttachmentError.ErrorCode.invalid_format:
            return f"Invalid attachment format: {self.format}"
        if self.ErrorCode == AttachmentError.ErrorCode.invalid_name:
            return f"Invalid attachment name: {self.name}"
        if self.ErrorCode == AttachmentError.ErrorCode.duplicate_name:
            return f"Duplicate attachment name: {self.name}"
        return "Attachment error"


class AttachmentFormat(Enum):
    """ Attachment format type """
    text = 1
    binary = 2


class Attachment: # pylint: disable=R0903
    """ Attachment class """

    _VALID_CHARS = "1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm_."
    _REPLACEMENT_CHAR = "_"

    def __init__(self,
                 p_name: str = None,
                 p_format: AttachmentFormat = AttachmentFormat.text,
                 p_text_content: str = None,
                 p_binary_content: bytearray = None):

        Validator.validate_attachment_format(p_format)

        if p_name is None:
            self._name = ""
        else:
            self._name = Attachment._cleanse_name(p_name)

        self.format = p_format

        if p_text_content is None:
            self.text_content = ""
        else:
            self.text_content = p_text_content

        self.binary_content = p_binary_content

    @property
    def name(self) -> str:
        """ Attachment name """
        return self._name

    @name.setter
    def name(self, p_val: str):
        """ Attachment name setter
        We cleanse the attachment name from invalid characters here
        """
        self._name = Attachment._cleanse_name(p_val)

    @staticmethod
    def guess_format_by_mime_type(p_mime_type: str) -> AttachmentFormat:
        """ Returns if attachment is text or binary """
        if any(["text" in p_mime_type,
                "txt" in p_mime_type,
                "html" in p_mime_type,
                "json" in p_mime_type,
                "application/xml" in p_mime_type]):
            return AttachmentFormat.text
        return AttachmentFormat.binary

    @staticmethod
    def guess_format_by_file_extension(p_extension: str) -> AttachmentFormat:
        """ Returns if attachment is text or binary """
        low_ext = p_extension.lower().replace(".", "")
        if low_ext in ["txt", "html", "json", "xml"]:
            return AttachmentFormat.text
        return AttachmentFormat.binary

    @staticmethod
    def guess_format_by_file_name(p_name: str) -> AttachmentFormat:
        """ Returns if attachment is text or binary """
        name_split = path.splitext(p_name)
        if len(name_split) < 2:
            return Attachment.guess_format_by_file_extension("")
        return Attachment.guess_format_by_file_extension(name_split[1])

    @staticmethod
    def _cleanse_name(p_val: str) -> str:
        output = ""
        for name_char in p_val:
            if name_char in Attachment._VALID_CHARS:
                output += name_char
            else:
                output += Attachment._REPLACEMENT_CHAR
        return output


class Validator:
    """ Attachment validator class """
    @staticmethod
    def ensure_all_names_are_unique(p_attachments: List[Attachment], p_correct: bool = True):
        """ Prevents duplicate file names among attachments """
        if p_correct:
            iter_count = 0
            while True:
                try:
                    Validator._enforce_names_are_unique(p_attachments)
                    return
                except Exception as error: # pylint: disable=W0703
                    iter_count += 1
                    if iter_count > 30:
                        raise error
                    Validator._rename_duplicates(p_attachments)
        else:
            Validator._enforce_names_are_unique(p_attachments)

    @staticmethod
    def _enforce_names_are_unique(p_attachments: List[Attachment]):
        name_count = {}
        for attachment in p_attachments:
            if attachment.name in name_count:
                name_count[attachment.name] += 1
            else:
                name_count[attachment.name] = 1

        for name, count in name_count.items():
            if count > 1:
                raise AttachmentError(AttachmentError.ErrorCode.duplicate_name, p_name=name)

    @staticmethod
    def _rename_duplicates(p_attachments: List[Attachment]):
        unique_names = []
        for attachment in p_attachments:
            if attachment.name not in unique_names:
                unique_names.append(attachment.name)

        for name in unique_names:
            name_count = 0
            for attachment in p_attachments:
                if attachment.name != name:
                    continue
                name_count += 1
                if name_count < 2:
                    continue
                att_name, att_extension = path.splitext(attachment.name)
                att_name += " (" + str(name_count) + ")"
                attachment.name = att_name + att_extension

    @staticmethod
    def validate_attachment_format(p_format: AttachmentFormat):
        """ Validates attachment format code """
        if p_format is None or p_format not in AttachmentFormat:
            raise AttachmentError(AttachmentError.ErrorCode.invalid_format, p_format=p_format)

    @staticmethod
    def validate_attachment_name(p_name: str):
        """ Validates attachment file name """
        if p_name is None or p_name == "":
            raise AttachmentError(AttachmentError.ErrorCode.invalid_name, p_name=p_name)

    @staticmethod
    def validate_attachments(p_attachments: List[Attachment]):
        """ Runs all validations for attachments """
        for attachment in p_attachments:
            Validator.validate_attachment_name(attachment.name)
            Validator.validate_attachment_format(attachment.format)
        Validator.ensure_all_names_are_unique(p_attachments)
