from enum import Enum
from typing import List


class AttachmentError(Exception):
    class ErrorCode(Enum):
        invalid_format: 1
        invalid_name: 2
        duplicate_name: 3

    def __init__(self, p_error_code: ErrorCode, p_format: str = None, p_name: str = None):
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
        if self.ErrorCode == AttachmentError.ErrorCode.invalid_format:
            return "Invalid attachment format: " + self.format
        if self.ErrorCode == AttachmentError.ErrorCode.invalid_name:
            return "Invalid attachment name: " + self.name
        if self.ErrorCode == AttachmentError.ErrorCode.duplicate_name:
            return "Duplicate attachment name: " + self.name
        return "Attachment error"


class AttachmentFormat(Enum):
    text = 1
    binary = 2


class Attachment:
    def __init__(self,
                 p_name: str = None,
                 p_format: AttachmentFormat = AttachmentFormat.text,
                 p_text_content: str = None,
                 p_binary_content: bytearray = None):

        Validator.validate_attachment_format(p_format)

        if p_name is None:
            self.name = ""
        else:
            self.name = p_name

        self.format = p_format

        if p_text_content is None:
            self.text_content = ""
        else:
            self.text_content = p_text_content

        self.binary_content = p_binary_content


class Validator:
    @staticmethod
    def ensure_all_names_are_unique(p_attachments: List[Attachment]):
        name_count = {}
        for attachment in p_attachments:
            if attachment.name in name_count:
                name_count[attachment.name] += 1
            else:
                name_count[attachment.name] = 1

        for name in name_count:
            if name_count[name] > 1:
                raise AttachmentError(AttachmentError.ErrorCode.duplicate_name, p_name=name)

    @staticmethod
    def validate_attachment_format(p_format: AttachmentFormat):
        if p_format is None or p_format not in AttachmentFormat:
            raise AttachmentError(AttachmentError.ErrorCode.invalid_format, p_format=p_format)

    @staticmethod
    def validate_attachment_name(p_name: str):
        if p_name is None or p_name == "":
            raise AttachmentError(AttachmentError.ErrorCode.invalid_name, p_name=p_name)

    @staticmethod
    def validate_attachments(p_attachments: List[Attachment]):
        for attachment in p_attachments:
            Validator.validate_attachment_name(attachment.name)
            Validator.validate_attachment_format(attachment.format)
        Validator.ensure_all_names_are_unique(p_attachments)
