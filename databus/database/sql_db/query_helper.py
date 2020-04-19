""" Query helper module """
from typing import List
import pymssql
from pymssql import Connection
from databus.database.sql_db.insert_builder import InsertBuilder
from databus.database.sql_db.sql_database_arguments import SqlDatabaseArguments
from databus.database.sql_db.update_builder import UpdateBuilder
from databus.database.sql_db.where_builder import WhereBuilder


class QueryHelper:
    """ Helper class to access SQL server easier """
    @staticmethod
    def open_new_connection(p_args: SqlDatabaseArguments) -> Connection:
        """ Opens a new connection """
        return pymssql.connect(server=p_args.server,
                               user=p_args.username,
                               password=p_args.password,
                               database=p_args.database)

    def __init__(self, p_arguments: dict, p_client_id: str):
        self._args = SqlDatabaseArguments(p_arguments)
        self._connection = QueryHelper.open_new_connection(self._args)
        self._client_id = p_client_id
        self._where = WhereBuilder(p_client_id=self._client_id)

    def delete(self, p_table: str, p_where: str = ""):
        """ Deletes entries from SQL server """
        command = "DELETE FROM " + p_table + self._where.build(p_where)
        self.execute_sql(command)

    def execute_insert(self, p_insert: InsertBuilder):
        """ Executes an Insert statement """
        self.execute_sql(p_insert.insert_command)

    def execute_sql(self, p_query: str):
        """ Executes an SQL command; typically for updating / deleting """
        cursor = self._connection.cursor()
        cursor.execute(p_query)

    def execute_update(self, p_update: UpdateBuilder):
        """ Executes an Insert statement """
        self.execute_sql(p_update.update_command)

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

    def select_all(self, p_table: str, p_where: str = "", p_order_fields: List[str] = None) -> dict:
        """ Selects & returns all entries from table
        The where condition will be touched - client id will be added automatically
        """
        where = self._where.build(p_where, p_order_fields=p_order_fields)
        return self.select_all_literal_where(p_table, p_literal_where=where)

    def select_all_literal_where(self, p_table: str, p_literal_where: str = "") -> dict:
        """ Selects & returns all entries from table
        The where condition is used as a literal value, so it's not polluted by
        client ID or anything.
        """
        query = "SELECT * FROM " + self.get_table_path(p_table) + p_literal_where
        cursor = self._connection.cursor(as_dict=True)
        cursor.execute(query)
        return cursor.fetchall()

    def select_all_no_where(self, p_table: str, p_order_by: str = "") -> dict:
        """ Selects & returns all entries from table, without WHERE conditions """
        query = "SELECT * FROM " + self.get_table_path(p_table)
        if p_order_by != "":
            query += " ORDER BY " + p_order_by
        cursor = self._connection.cursor(as_dict=True)
        cursor.execute(query)
        return cursor.fetchall()

    def select_all_where_builder(self, p_table: str, p_builder: WhereBuilder) -> dict:
        """ Selects & returns all entries from table which match the builder """
        return self.select_all_literal_where(p_table, p_builder.where)

    def select_single(self, p_table: str, p_where: str = "") -> dict:
        """ Selects & returns a single entry
        The where condition will be touched - client id will be added automatically
        """
        where = self._where.build(p_where)
        return self.select_all_literal_where(p_table, p_literal_where=where)[0]
