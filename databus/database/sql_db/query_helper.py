""" Query helper module """
from typing import List
import pyodbc
from databus.database.sql_db.insert_builder import InsertBuilder
from databus.database.sql_db.path_builder import PathBuilder
from databus.database.sql_db.sql_database_arguments import SqlDatabaseArguments
from databus.database.sql_db.update_builder import UpdateBuilder
from databus.database.sql_db.where_builder import WhereBuilder

# todo
# her şeyi commit etmek yerine bir kerede commit
# log gibi toplu insert'lerde birer birer insert yerine itab yollamak?
# pyodbc nasıl hızlanır?
# database temizle

class QueryHelper:
    """ Helper class to access SQL server easier """
    @staticmethod
    def open_new_connection(p_args: SqlDatabaseArguments):
        """ Opens a new connection """
        return pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};"
                              "SERVER=" + p_args.server + ";"
                              "DATABASE=" + p_args.database + ";"
                              "UID=" + p_args.username + ";"
                              "PWD=" + p_args.password)

    def __init__(self, p_arguments: dict, p_client_id: str):
        self.args = SqlDatabaseArguments(p_arguments)
        self._connection = QueryHelper.open_new_connection(self.args)
        self._cursor = self._connection.cursor()
        self._client_id = p_client_id
        self._where = WhereBuilder(p_client_id=self._client_id)
        self._path_builder = PathBuilder(self.args)

    def delete(self, p_table: str, p_where: str = ""):
        """ Deletes entries from SQL server """
        command = "DELETE FROM " + self._path_builder.get_table_path(p_table) + self._where.build(p_where)
        self.execute_sql(command)

    def execute_insert(self, p_insert: InsertBuilder):
        """ Executes an Insert statement """
        self.execute_sql(p_insert.insert_command)

    def execute_sql(self, p_query: str):
        """ Executes an SQL command; typically for updating / deleting """
        self._cursor.execute(p_query)
        self._connection.commit()

    def execute_update(self, p_update: UpdateBuilder):
        """ Executes an Insert statement """
        self.execute_sql(p_update.update_command)

    def select_all(self, p_table: str, p_where: str = "", p_order_fields: List[str] = None) -> dict:
        """ Selects & returns all entries from table
        The where condition will be touched - client id will be added automatically
        """
        where = self._where.build(p_where, p_order_fields=p_order_fields)
        return self.select_all_literal_where(p_table, p_literal_where=where)

    def select_all_literal_where(self, p_table: str, p_literal_where: str = "") -> List[dict]:
        """ Selects & returns all entries from table
        The where condition is used as a literal value, so it's not polluted by
        client ID or anything.
        """
        query = "SELECT * FROM " + self._path_builder.get_table_path(p_table) + p_literal_where
        return self._select(query)

    def select_all_no_where(self, p_table: str, p_order_by: str = "") -> dict:
        """ Selects & returns all entries from table, without WHERE conditions """
        query = "SELECT * FROM " + self._path_builder.get_table_path(p_table)
        if p_order_by != "":
            query += " ORDER BY " + p_order_by
        return self._select(query)

    def select_all_where_builder(self, p_table: str, p_builder: WhereBuilder) -> dict:
        """ Selects & returns all entries from table which match the builder """
        return self.select_all_literal_where(p_table, p_builder.where)

    def select_single(self, p_table: str, p_where: str = "") -> dict:
        """ Selects & returns a single entry
        The where condition will be touched - client id will be added automatically
        """
        where = self._where.build(p_where)
        return self.select_all_literal_where(p_table, p_literal_where=where)[0]

    def _select(self, p_query: str) -> List[dict]:
        output = []
        self._cursor.execute(p_query)
        results = self._cursor.fetchall()
        for result in results:
            output_item = {}
            index = 0
            for description in result.cursor_description:
                output_item[description[0]] = result[index]
                index += 1
            output.append(output_item)
        return output
