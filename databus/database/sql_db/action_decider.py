""" Module for deciding on SQL actions """
from enum import Enum
from databus.database.sql_db.delete_builder import DeleteBuilder
from databus.database.sql_db.insert_builder import InsertBuilder
from databus.database.sql_db.update_builder import UpdateBuilder
from databus.database.sql_db.query_helper import QueryHelper
from databus.database.sql_db.table import Table


class Action(Enum):
    """ Defines a database action """
    INSERT = 1
    UPDATE = 2
    DELETE = 3


class ActionDecision:
    """ Action decision class
    Basically; this is the output of ActionDecider
    """
    def __init__(self, p_query_helper: QueryHelper):
        self.inserts = []
        self.updates = []
        self.deletes = []
        self._query_helper = p_query_helper

    def add_delete(self, p_table: str, p_row: dict):
        """ Adds a new delete command """
        delete = DeleteBuilder(self._query_helper.args, self._query_helper.client_id)
        delete.table = p_table
        key_fields = Table(self._query_helper, p_table).key_fields

        for key_field in key_fields:
            cell_value = p_row[key_field]
            if key_field == "client_id":
                assert cell_value == self._query_helper.client_id
                continue
            if isinstance(cell_value, int):
                delete.where.add_and_field_eq_int(key_field, cell_value)
            else:
                delete.where.add_and_field_eq_str(key_field, cell_value)

        self.deletes.append(delete)

    def add_insert(self, p_table: str, p_row: dict):
        """ Adds a new insert command """
        insert = InsertBuilder(self._query_helper.args, self._query_helper.client_id)
        insert.table = p_table

        for table_col in p_row:
            cell_value = p_row[table_col]
            if table_col == "client_id":
                assert cell_value == self._query_helper.client_id
                continue
            if isinstance(cell_value, int):
                insert.add_int(table_col, cell_value)
            else:
                insert.add_string(table_col, cell_value)

        self.inserts.append(insert)

    def add_update(self, p_table: str, p_row: dict):
        """ Adds a new update command """
        update = UpdateBuilder(self._query_helper.args, self._query_helper.client_id)
        update.table = p_table
        key_fields = Table(self._query_helper, p_table).key_fields

        for table_col in p_row:
            cell_value = p_row[table_col]
            if table_col == "client_id":
                assert cell_value == self._query_helper.client_id
                continue

            if table_col in key_fields:
                if isinstance(cell_value, int):
                    update.where.add_and_field_eq_int(table_col, cell_value)
                else:
                    update.where.add_and_field_eq_str(table_col, cell_value)
            else:
                if isinstance(cell_value, int):
                    update.add_int(table_col, cell_value)
                else:
                    update.add_string(table_col, cell_value)

        self.updates.append(update)


class AnalysisResult(Enum):
    """ Analysis result """
    NOT_FOUND = 1
    MODIFIED = 2
    SAME = 3


class ActionDecider: # pylint: disable=R0903
    """ Action decider class
    This class will take 2 dictionaries.
    A) Dictionary in memory
    B) Dictionary in database
    It will compare both, and tell what needs to be inserted / updated / deleted
    """
    def __init__(self, p_query_helper: QueryHelper):
        self._memory = {}
        self._database = {}
        self._query_helper = p_query_helper
        self._decision = ActionDecision(self._query_helper)

    def decide(self, p_memory: dict, p_database: dict) -> ActionDecision:
        """ Decides what action(s) to take """
        self._memory = p_memory
        self._database = p_database
        self._decision = ActionDecision(self._query_helper)

        self._compare_database_with_memory()
        self._compare_memory_with_database()
        return self._decision

    def _analyse(self, p_table_name: str, p_src_line: dict, p_tar: dict) -> AnalysisResult:
        """ Runs an analysis """

        if p_table_name not in p_tar:
            return AnalysisResult.NOT_FOUND
        tar_lines = p_tar[p_table_name]

        key_fields = Table(self._query_helper, p_table_name).key_fields

        target_found = False
        for tar_line in tar_lines:
            this_is_target_line = True
            for key_field in key_fields:
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

    def _compare_database_with_memory(self):
        for table_name in self._database:
            for table_row in self._database[table_name]:
                result = self._analyse(
                    table_name,
                    table_row,
                    self._memory)

                if result == AnalysisResult.NOT_FOUND:
                    self._decision.add_delete(table_name, table_row)

    def _compare_memory_with_database(self):
        for table_name in self._memory:
            for table_row in self._memory[table_name]:
                result = self._analyse(
                    table_name,
                    table_row,
                    self._database)

                if result == AnalysisResult.MODIFIED:
                    self._decision.add_update(table_name, table_row)
                if result == AnalysisResult.NOT_FOUND:
                    self._decision.add_insert(table_name, table_row)
