""" Module for deciding on SQL actions """
from typing import List
from databus.client.client import Client
from databus.database.difference_check import DifferenceChecker, TableKey, Action
from databus.database.sql_db.delete_builder import DeleteBuilder
from databus.database.sql_db.insert_builder import InsertBuilder
from databus.database.sql_db.update_builder import UpdateBuilder
from databus.database.sql_db.query_helper import QueryHelper
from databus.database.sql_db.table import Table


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
        delete = DeleteBuilder(
            self._query_helper.args,
            self._get_modifiable_client_id(p_table, p_row))
        delete.table = p_table
        key_fields = Table(self._query_helper, p_table).key_fields

        for key_field in key_fields:
            cell_value = p_row[key_field]
            if key_field == "client_id":
                self._validate_client_id(cell_value)
                continue
            if isinstance(cell_value, int):
                delete.where.add_and_field_eq_int(key_field, cell_value)
            else:
                delete.where.add_and_field_eq_str(key_field, cell_value)

        self.deletes.append(delete)

    def add_insert(self, p_table: str, p_row: dict):
        """ Adds a new insert command """
        insert = InsertBuilder(
            self._query_helper.args,
            self._get_modifiable_client_id(p_table, p_row))
        insert.table = p_table

        for table_col in p_row:
            cell_value = p_row[table_col]
            if table_col == "client_id":
                self._validate_client_id(cell_value)
                continue
            if isinstance(cell_value, int):
                insert.add_int(table_col, cell_value)
            else:
                insert.add_string(table_col, cell_value)

        self.inserts.append(insert)

    def add_update(self, p_table: str, p_row: dict):
        """ Adds a new update command """
        update = UpdateBuilder(
            self._query_helper.args,
            self._get_modifiable_client_id(p_table, p_row))

        update.table = p_table
        key_fields = Table(self._query_helper, p_table).key_fields

        for table_col in p_row:
            cell_value = p_row[table_col]
            if table_col == "client_id":
                self._validate_client_id(cell_value)
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

    def _get_modifiable_client_id(self, p_table: str, p_row: dict):
        if p_table == "client" and self._query_helper.client_id == Client.ROOT:
            return p_row["client_id"]
        return self._query_helper.client_id

    def _validate_client_id(self, p_client_id: str):
        if self._query_helper.client_id == Client.ROOT:
            return
        assert p_client_id == self._query_helper.client_id


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

        table_keys = self._get_table_keys(p_database)
        diff_checker = DifferenceChecker(table_keys, p_memory, p_database)

        for difference in diff_checker.result:
            if difference.action == Action.INSERT:
                self._decision.add_insert(difference.table, difference.row)
            elif difference.action == Action.UPDATE:
                self._decision.add_update(difference.table, difference.row)
            elif difference.action == Action.DELETE:
                self._decision.add_delete(difference.table, difference.row)

        return self._decision

    def decide_and_execute(self, p_memory: dict, p_database: dict):
        """ Decides what action(s) to take, and executes them """
        decision = self.decide(p_memory, p_database)

        try:
            action_taken = False

            for insert in decision.inserts:
                self._query_helper.execute_insert(insert)
                action_taken = True

            for update in decision.updates:
                self._query_helper.execute_update(update)
                action_taken = True

            for delete in decision.deletes:
                self._query_helper.execute_delete(delete)
                action_taken = True

            if action_taken:
                self._query_helper.commit()

        except Exception as error:
            self._query_helper.rollback()
            raise error

    def _get_table_keys(self, p_database: dict) -> List[TableKey]:
        output = []
        for table_name in p_database:
            table_obj = Table(self._query_helper, table_name)
            table_keys = table_obj.key_fields
            table_key_obj = TableKey(table_name, table_keys)
            output.append(table_key_obj)
        return output
