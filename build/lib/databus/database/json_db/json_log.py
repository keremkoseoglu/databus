""" JSON log module """
from datetime import datetime
from os import path, remove, scandir
from typing import List
from databus.client.log import Log
from databus.database.json_db.json_client import JsonClient
from databus.database.json_db.json_database_arguments import JsonDatabaseArguments
from databus.database.json_db.json_path_builder import JsonPathBuilder


class JsonLog:
    """ JSON log class """
    def __init__(self, args: JsonDatabaseArguments):
        self._args = args
        self._client = JsonClient(args)

    def build_log_file_name(self, p_log: Log) -> str:
        """ Builds log file name """
        datetime_part = p_log.creation_datetime.isoformat()
        safe_datetime_part = datetime_part.replace(":", "_")
        guid_part = str(p_log.guid)
        return safe_datetime_part + "_" + guid_part + "." + self._args.log_extension

    def build_log_file_path(self, p_client_id: str, p_log: Log) -> str:
        """ Builds log file path """
        return path.join(self.get_root_path(p_client_id),
                         self.build_log_file_name(p_log))

    def delete_log_file_before(self, p_client_id: str, p_before: datetime, p_log: Log):
        """ Deletes log files before the given date """
        log_root_path = self.get_root_path(p_client_id)
        all_log_files = self.get_log_file_list(p_client_id)
        for log_file in all_log_files:
            split1 = log_file.split("T")
            split2 = split1[0].split("-")
            log_file_date = datetime(year=int(split2[0]), month=int(split2[1]), day=int(split2[2]))
            if log_file_date < p_before:
                full_log_file_path = path.join(log_root_path, log_file)
                p_log.append_text("Deleting " + full_log_file_path)
                remove(full_log_file_path)

    def get_log_file_content(self, p_client_id: str, p_log_file: str) -> str:
        """ Returns the content of the given log file """
        output = ""
        log_path = path.join(self.get_root_path(p_client_id), p_log_file)
        with open(log_path, mode="r") as log_file:
            output = log_file.read()
        return output

    def get_log_file_list(self, p_client_id: str) -> List[str]:
        """ Log file list """
        output = []
        log_root_path = self.get_root_path(p_client_id)
        file_list = [f.name for f in scandir(log_root_path) if f.is_file()]
        supposed_extension = self._args.log_extension.lower()
        for file_candidate in file_list:
            extension = path.splitext(file_candidate)[1].replace(".", "").lower()
            if extension == supposed_extension:
                output.append(file_candidate)
        return output

    def get_root_path(self, p_client_id: str) -> str:
        """ Returns the root log path for the given client """
        return self._get_path_builder(p_client_id).log_root_path

    def insert(self, p_client_id: str, p_log: Log):
        """ Writes log file to disk """
        log_file_content = p_log.entries_as_string
        log_file_path = self.build_log_file_path(p_client_id, p_log)

        log_file = open(log_file_path, "w+")
        log_file.write(log_file_content)
        log_file.close()

    def _get_path_builder(self, p_client_id: str) -> JsonPathBuilder:
        return JsonPathBuilder(p_client_id, self._args)
