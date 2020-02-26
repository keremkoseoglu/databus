from enum import Enum


class AttachmentError(Exception):
    class ErrorCode(Enum):
        invalid_format: 1

    def __init__(self, p_error_code: ErrorCode, p_format: str = None):
        self.error_code = p_error_code

        if p_format is None:
            self.format = ""
        else:
            self.format = p_format

    @property
    def message(self) -> str:
        if self.ErrorCode == AttachmentError.ErrorCode.invalid_format:
            return "Invalid attachment format: " + self.format
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

        if p_format is None or p_format not in AttachmentFormat:
            raise AttachmentError(AttachmentError.ErrorCode.invalid_format, p_format=p_format)

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
