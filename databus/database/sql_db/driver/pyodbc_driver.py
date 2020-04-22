""" Module for connecting to SQL Server over PYODBC """
from typing import List
import pyodbc
from databus.database.sql_db.sql_database_arguments import SqlDatabaseArguments
from databus.database.sql_db.driver.abstract_driver import SqlServerDriver


class PyodbcDriver(SqlServerDriver):
    """ PYODBC driver for SQL Server """

    def __init__(self):
        super().__init__()
        self._connection = None
        self._cursor = None

    def commit(self):
        """ Commits the transactions """
        self._connection.commit()

    def connect(self, p_args: SqlDatabaseArguments):
        """ Opens a new connection to the database """
        self._connection = pyodbc.connect( # pylint: disable=I1101
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=" + p_args.server + ";"
            "DATABASE=" + p_args.database + ";"
            "UID=" + p_args.username + ";"
            "PWD=" + p_args.password + ";")

        self._cursor = self._connection.cursor()

    def execute_sql(self, p_query: str):
        """ Executes the given SQL
        Also commits if self.autocommit is true
        """
        self._cursor.execute(p_query)
        if self.autocommit:
            self.commit()

    def execute_stored_procedure(self, p_sql: str, p_values):
        """ Executes a stored procedure """
        self._cursor.execute(p_sql, (p_values))

    def rollback(self):
        """ Rollbacks the transactions """
        self._connection.rollback()

    def select(self, p_query: str) -> List[dict]:
        """ Selects data from the database """
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
