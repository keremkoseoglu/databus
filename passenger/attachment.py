from enum import Enum


class AttachmentFormat(Enum):
    text = 1
    binary = 2


class Attachment:
    name: str
    format: AttachmentFormat
    text_content: str
    binary_content: bytearray

    def __init__(self,
                 p_name: str = "",
                 p_format: AttachmentFormat = AttachmentFormat.text,
                 p_text_content: str = "",
                 p_binary_content: bytearray = ()):
        self.name = p_name
        self.format = p_format
        self.text_content = p_text_content
        self.binary_content = p_binary_content
