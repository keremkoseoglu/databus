""" Customizing node backup """
from datetime import datetime
from os import listdir, path, remove
import uuid
import pathlib
from databus.client.customizing import ClientCustomizing
from databus.client.log import Log, LogEntry, MessageType
from databus.database.json_db.json_database_arguments import JsonDatabaseArguments
from databus.database.json_db.json_path_builder import JsonPathBuilder
from databus.database.abstract_database import AbstractDatabase

class CustomizingNodeBackup:
    """ Customizing node backup """
    def __init__(self, json_db_arguments: JsonDatabaseArguments):
        self._args = json_db_arguments

    def execute(self, p_cc: ClientCustomizing):
        """ Executes main operation """
        path_builder = JsonPathBuilder(p_cc.client.id, p_args=self._args)
        pathlib.Path(path_builder.backup_root_path).mkdir(parents=True, exist_ok=True)
        backup_id = str(uuid.uuid4())

        for node in p_cc.nodes:
            node_file = f"{backup_id}-{node.name}.json"
            node_path = path.join(path_builder.backup_root_path, node_file)
            with open(node_path, "w", encoding="utf-8") as open_node_path:
                open_node_path.write(node.content)

    def delete_old_files(self, p_before: datetime, p_db: AbstractDatabase, p_log: Log):
        """ Deletes expired backup files """
        clients = p_db.get_clients()

        for client in clients:
            path_builder = JsonPathBuilder(client.id, p_args=self._args)
            bak_path = path_builder.backup_root_path
            bak_files = [f for f in listdir(bak_path) if path.isfile(path.join(bak_path, f))]

            for bak_file in bak_files:
                try:
                    bak_file_path = path.join(bak_path, bak_file)
                    create_ctime = path.getctime(bak_file_path)
                    create_dt = datetime.fromtimestamp(create_ctime)

                    if create_dt > p_before:
                        continue

                    remove(bak_file_path)

                except Exception as error:
                    if p_log is None:
                        continue
                    log_entry = LogEntry(p_message=str(error), p_type=MessageType.error)
                    p_log.append_entry(log_entry)
