from databus.client.log import Log
from databus.database.json_db.json_client import JsonClient
from databus.database.json_db.json_database_arguments import JsonDatabaseArguments
from datetime import datetime
from os import path, remove, scandir
from typing import List


class JsonLog:

    @staticmethod
    def _build_log_file_content(p_log: Log) -> str:
        output = ""
        for entry in p_log.entries:
            new_line = "[" + entry.timestamp.isoformat() + "]"
            new_line += "[" + entry.source + "]"
            new_line += "[" + str(entry.type.name) + "]"
            new_line += " " + entry.message
            if output != "":
                output += "\r\n"
            output += new_line
        return output

    def __init__(self, args: JsonDatabaseArguments):
        self._args = args
        self._client = JsonClient(args)

    def build_log_file_name(self, p_log: Log) -> str:
        datetime_part = p_log.creation_datetime.isoformat()
        guid_part = str(p_log.guid)
        return datetime_part + "_" + guid_part + "." + self._args.log_extension

    def build_log_file_path(self, p_client_id: str, p_log: Log) -> str:
        return path.join(self.build_log_root_path(p_client_id),
                         self.build_log_file_name(p_log))

    def build_log_root_path(self, p_client_id: str) -> str:
        return path.join(self._client.build_client_dir_path(p_client_id),
                         self._args.log_dir)

    def delete_log_file_before(self, p_client_id: str, p_before: datetime, p_log: Log):
        log_root_path = self.build_log_root_path(p_client_id)
        all_log_files = self.get_log_file_list(p_client_id)
        for log_file in all_log_files:
            split1 = log_file.split("T")
            split2 = split1[0].split("-")
            log_file_date = datetime(year=int(split2[0]), month=int(split2[1]), day=int(split2[2]))
            if log_file_date < p_before:
                full_log_file_path = path.join(log_root_path, log_file)
                p_log.append_text("Deleting " + full_log_file_path)
                remove(full_log_file_path)

    def get_log_file_list(self, p_client_id: str) -> List[str]:
        log_root_path = self.build_log_root_path(p_client_id)
        return [f.name for f in scandir(log_root_path) if f.is_file()]

    def insert(self, p_client_id: str, p_log: Log):
        log_file_content = JsonLog._build_log_file_content(p_log)
        log_file_path = self.build_log_file_path(p_client_id, p_log)

        log_file = open(log_file_path, "w+")
        log_file.write(log_file_content)
        log_file.close()
