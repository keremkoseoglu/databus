from database.abstract_database import AbstractDatabase
from database.json_database import JsonDatabase


class DatabaseFactory:
    __singleton: AbstractDatabase = None

    @staticmethod
    def get_instance() -> AbstractDatabase:
        if DatabaseFactory.__singleton is None:
            DatabaseFactory.__singleton = JsonDatabase()
        return DatabaseFactory.__singleton
