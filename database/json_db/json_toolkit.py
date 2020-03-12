from datetime import datetime


class JsonToolkit:
    @staticmethod
    def convert_json_date_to_datetime(p_json_date: str) -> datetime:
        return datetime.strptime(p_json_date, '%Y-%m-%dT%H:%M:%S.%f')
