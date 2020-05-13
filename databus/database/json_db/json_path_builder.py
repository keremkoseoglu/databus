""" Path builder module """
from os import path, scandir
from typing import List
from databus import get_root_path
from databus.database.json_db.json_database_arguments import JsonDatabaseArguments

class JsonPathBuilder:
    """ JSON path builder class """

    @staticmethod
    def get_client_root_path(p_args: JsonDatabaseArguments) -> str:
        """ Builds the concrete root path of client directories """
        databus_root = get_root_path()
        return path.join(databus_root, p_args.database_dir, p_args.client_dir)

    def __init__(self, p_client_id: str, p_args: JsonDatabaseArguments):
        self._client_id = p_client_id
        self._args = p_args

    @property
    def client_root_path(self) -> str:
        """ Returns root path of client """
        return JsonPathBuilder.get_client_root_path(self._args)

    @property
    def client_dir_path(self) -> str:
        """ Builds the concrete path for client directory """
        client_root_path = self.client_root_path
        return path.join(client_root_path, self._client_id)

    @property
    def config_file_path(self) -> str:
        """ Returns the config file path """
        return path.join(
            self.client_dir_path,
            self._args.client_config)

    @property
    def log_root_path(self) -> str:
        """ Builds log file root path """
        return path.join(self.client_dir_path,
                         self._args.log_dir)

    @property
    def passenger_directories(self) -> List[str]:
        """ Returns all passenger directories of client """
        return [f.name for f in scandir(self.queue_root_path) if f.is_dir()]

    @property
    def queue_root_path(self) -> str:
        """ Returns the root path of the queue dir """
        return path.join(
            self.client_dir_path,
            self._args.queue_dir)

    def get_attachment_directory_path(self, p_internal_id: str) -> str:
        """ Returns the attachment directory path """
        return path.join(
            self.queue_root_path,
            p_internal_id,
            self._args.queue_attachment_dir)

    def get_attachment_file_path(self, p_internal_id: str, p_file_name: str) -> str:
        """ Returns the path of the given attachment file """
        return path.join(
            self.get_attachment_directory_path(p_internal_id),
            p_file_name)

    def get_passenger_directory_path(self, p_internal_id: str) -> str:
        """ Returns the path of the given passenger directory """
        return path.join(
            self.queue_root_path,
            p_internal_id)

    def get_passenger_file_path(self, p_internal_id: str) -> str:
        """ Returns passenger file path """
        return path.join(
            self.queue_root_path,
            p_internal_id,
            self._args.queue_passenger)
