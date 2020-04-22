""" Module for an abstract SQL Server driver """
from abc import ABC, abstractmethod
from typing import List
from databus.database.sql_db.sql_database_arguments import SqlDatabaseArguments


class SqlServerDriver(ABC):
    """ Abstract SQL Server driver class """

    def __init__(self):
        self.autocommit = True

    @abstractmethod
    def commit(self):
        """ Commits the transactions """

    @abstractmethod
    def connect(self, p_args: SqlDatabaseArguments):
        """ Opens a new connection to the database """

    @abstractmethod
    def execute_stored_procedure(self, p_sql: str, p_values):
        """ Executes a stored procedure """

    @abstractmethod
    def execute_sql(self, p_query: str):
        """ Executes the given SQL
        Also commits if self.autocommit is true
        """

    @abstractmethod
    def rollback(self):
        """ Rollbacks the transactions """

    @abstractmethod
    def select(self, p_query: str) -> List[dict]:
        """ Selects data from the database """
