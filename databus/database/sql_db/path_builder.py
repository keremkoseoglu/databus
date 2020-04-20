""" Path builder module
This module includes helper methods to build
table & field paths
"""
from databus.database.sql_db.sql_database_arguments import SqlDatabaseArguments


class PathBuilder:
    """ Path builder class for table & field paths """
    def __init__(self, p_args: SqlDatabaseArguments):
        self._args = p_args

    def get_field_path(self, p_table: str, p_field: str) -> str:
        """ Returns the full path of the table field
        DATABASE.SCHEMA.TABLE.FIELD
        """
        return self.get_table_path(p_table) + "." + p_field

    def get_table_path(self, p_table: str) -> str:
        """ Returns the full path of the table
        DATABASE.SCHEMA.TABLE
        """
        return self._args.database + "." + self._args.schema + "." + p_table
