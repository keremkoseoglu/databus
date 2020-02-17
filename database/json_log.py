from client.log import Log
from database.json_client import *
import json


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


def build_log_file_name(p_log: Log) -> str:
    datetime_part = p_log.creation_datetime.isoformat()
    guid_part = str(p_log.guid)
    return datetime_part + "_" + guid_part + "." + JSON_DB_LOG_EXTENSION


def build_log_file_path(p_log: Log) -> str:
    return path.join(build_client_dir_path(p_log.client), JSON_DB_LOG_DIR, build_log_file_name(p_log))
