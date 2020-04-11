""" Generic JSON utility module """
from datetime import datetime


class JsonToolkit: # pylint: disable=R0903
    """ Generic JSON utility class """
    @staticmethod
    def convert_json_date_to_datetime(p_json_date: str) -> datetime:
        """ Converts JSON date string to PYTHON date time """
        return datetime.strptime(p_json_date, '%Y-%m-%dT%H:%M:%S.%f')
