""" Module for external configuration files """
from typing import List


class ExternalConfigFile: # pylint: disable=R0903
    """ External configuration file """
    def __init__(self, p_client_id: str, p_file_id: str, p_path: str):
        self.client_id = p_client_id
        self.file_id = p_file_id
        self.path = p_path

    @property
    def file_content(self) -> str:
        """ Reads file content from the disk & returns """
        with open(self.path, "r") as text_file:
            output = text_file.read()
        return output

    @file_content.setter
    def file_content(self, p_content: str):
        """ Writes file content to disk """
        with open(self.path, "w") as text_file:
            text_file.write(p_content)


class ExternalConfigFileManager:
    """ Manager of external configuration files """
    def __init__(self):
        self._files = {}

    def add_file(self, p_client_id: str, p_file_id: str, p_path: str):
        """ Registers a new file """
        file_key = ExternalConfigFileManager._build_file_key(p_client_id, p_file_id)
        file_obj = ExternalConfigFile(p_client_id, p_file_id, p_path)
        self._files[file_key] = file_obj

    def add_files(self, p_files: List[ExternalConfigFile]):
        """ Registers multiple files """
        for file in p_files:
            file_key = ExternalConfigFileManager._build_file_key(file.client_id, file.file_id)
            self._files[file_key] = file

    def get_file(self, p_client_id: str, p_file_id: str) -> ExternalConfigFile:
        """ Returns an existing file """
        file_key = ExternalConfigFileManager._build_file_key(p_client_id, p_file_id)
        return self._files[file_key]

    def get_files_of_client(self, p_client_id: str) -> List[ExternalConfigFile]:
        """ Returns all files of given client """
        output = []
        for file_key in self._files:
            file_obj = self._files[file_key]
            if file_obj.client_id == p_client_id:
                output.append(file_obj)
        return output

    @staticmethod
    def _build_file_key(p_client_id: str, p_file_id: str) -> str:
        return p_client_id + "__" + p_file_id
