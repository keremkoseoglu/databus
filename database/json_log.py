from client.log import Log
from config.constants import *
from database.json_client import JsonClient
from os import path


class JsonLog:
    @staticmethod
    def build_log_file_content(p_log: Log) -> str:
        output = ""
        for entry in p_log.entries:
            new_line = "[" + entry.timestamp.isoformat() + "]"
            new_line += "[" + str(entry.type.name) + "]"
            new_line += " " + entry.message
            if output != "":
                output += "\r\n"
            output += new_line
        return output

    @staticmethod
    def build_log_file_name(p_log: Log) -> str:
        datetime_part = p_log.creation_datetime.isoformat()
        guid_part = str(p_log.guid)
        return datetime_part + "_" + guid_part + "." + JSON_DB_LOG_EXTENSION

    @staticmethod
    def build_log_file_path(p_log: Log) -> str:
        return path.join(JsonClient.build_client_dir_path(p_log.client),
                         JSON_DB_LOG_DIR,
                         JsonLog.build_log_file_name(p_log))
