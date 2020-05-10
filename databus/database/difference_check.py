""" Module to check differences between memory and database states """
from enum import Enum
from typing import List


class Action(Enum):
    """ Defines a database action """
    INSERT = 1
    UPDATE = 2
    DELETE = 3


class AnalysisResult(Enum):
    """ Analysis result """
    NOT_FOUND = 1
    MODIFIED = 2
    SAME = 3


class DifferenceResult: # pylint: disable=R0903
    """ Result of a difference check """
    def __init__(self, p_table: str, p_row: dict, p_action: Action):
        self.table = p_table
        self.row = p_row
        self.action = p_action


class TableKey: # pylint: disable=R0903
    """ A list of table keys """
    def __init__(self, p_table: str, p_keys: List[str]):
        self.table = p_table
        self.keys = p_keys


class DifferenceChecker: # pylint: disable=R0903
    """ Class to check differences between memory and database states
    This class will take 2 dictionaries.
    A) Dictionary in memory
    B) Dictionary in database
    It will compare both, and tell what needs to be inserted / updated / deleted
    """

    def __init__(self, p_keys: List[TableKey], p_memory: dict, p_database: dict):
        self._result = []
        self._table_keys = p_keys
        self._memory = p_memory
        self._database = p_database
        self._compare_database_with_memory()
        self._compare_memory_with_database()

    @property
    def result(self) -> List[DifferenceResult]:
        """ Returns the result of the class """
        return self._result

    def _analyse(self, p_table_name: str, p_src_line: dict, p_tar: dict) -> AnalysisResult:
        if p_table_name not in p_tar:
            return AnalysisResult.NOT_FOUND
        tar_lines = p_tar[p_table_name]

        table_key = None
        for table_key_candidate in self._table_keys:
            if table_key_candidate.table == p_table_name:
                table_key = table_key_candidate
                break

        if table_key is None:
            raise Exception("No key provided for table " + p_table_name)

        target_found = False
        for tar_line in tar_lines:
            this_is_target_line = True
            for key_field in table_key.keys:
                if p_src_line[key_field] != tar_line[key_field]:
                    this_is_target_line = False
                    break
            if not this_is_target_line:
                continue
            target_found = True

            for column in tar_line:
                if p_src_line[column] != tar_line[column]:
                    return AnalysisResult.MODIFIED

        if target_found:
            return AnalysisResult.SAME
        return AnalysisResult.NOT_FOUND

    def _compare_memory_with_database(self):
        for table_name in self._memory:
            for table_row in self._memory[table_name]:
                result = self._analyse(
                    table_name,
                    table_row,
                    self._database)

                if result == AnalysisResult.MODIFIED:
                    diff_result = DifferenceResult(table_name, table_row, Action.UPDATE)
                    self._result.append(diff_result)
                if result == AnalysisResult.NOT_FOUND:
                    diff_result = DifferenceResult(table_name, table_row, Action.INSERT)
                    self._result.append(diff_result)

    def _compare_database_with_memory(self):
        for table_name in self._database:
            for table_row in self._database[table_name]:
                result = self._analyse(
                    table_name,
                    table_row,
                    self._memory)

                if result == AnalysisResult.NOT_FOUND:
                    diff_result = DifferenceResult(table_name, table_row, Action.DELETE)
                    self._result.append(diff_result)
