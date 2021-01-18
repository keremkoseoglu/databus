""" HTML link downloader module """
from typing import List
import os
import requests
from urlextract import URLExtract
from databus.passenger.attachment import Attachment, AttachmentFormat

class HtmlLinkDownloader:
    """ Scans the given HTML file, finds links, downloads
    the files and saves them as attachments.
    This method supports only text attachments at this time.
    """
    def __init__(self):
        self._extensions = []
        self._attachments = []

    def execute(self, p_attachments: List[Attachment], p_html: str, p_extensions: List[str]):
        """ Main method """
        self._extensions = p_extensions
        self._attachments = p_attachments
        urls = HtmlLinkDownloader._extract_urls(p_html)

        for url in urls:
            low_url = url.lower()
            if not self._has_eligible_extension(low_url):
                continue
            clean_url = HtmlLinkDownloader._clean_url(low_url)
            self._download(clean_url)

    @staticmethod
    def _extract_urls(p_html: str):
        # Build clean HTML
        if p_html is None or len(p_html) <= 0:
            return []
        clean_html = p_html.replace("\r", "").replace("\n", "")
        html_tag_pos = clean_html.lower().find("<html")
        if html_tag_pos < 0:
            return []
        clean_html = clean_html[html_tag_pos:]

       # Extract URL's
        extractor = URLExtract()
        urls = extractor.find_urls(clean_html)
        return urls

    @staticmethod
    def _clean_url(url):
        if "urldefense.com" in url:
            real_http_pos = url.rfind("http")
            clean_url = url[real_http_pos:].replace("__", "")
        else:
            clean_url = url
        if clean_url[-1] == "/":
            clean_url = clean_url[:-1]
        return clean_url

    def _has_eligible_extension(self, url):
        has_eligible_extension = False
        for extension in self._extensions:
            low_extension = "." + extension.lower()
            if low_extension in url:
                has_eligible_extension = True
                break
        return has_eligible_extension

    def _download(self, url):
        filename = os.path.basename(url)
        dummy_name, extension = os.path.splitext(filename)
        extension = extension.replace(".", "")
        file_format = Attachment.guess_format_by_file_extension(extension)

        response = requests.get(url, allow_redirects=True)

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

        self._attachments.append(downloaded_attachment)
