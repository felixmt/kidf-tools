"""modules import
"""
from tools.sql_helper import sql_helper

class notifier_helper:
    """app notifier helper
    """

    def __init__(self, db_env: str):
        self.sql_tools = sql_helper(db_env)

    def write_notifications(self, messages: list[dict]):
        """function to create db model
        """
        schema_monitoring = "data_monitoring"
        monitoring_query = f"INSERT INTO {schema_monitoring}.job_status VALUES \
                    (%(database)s, %(data_source)s, %(dataset)s, %(dataset_date)s,\
                    %(is_success)s, now(), %(rows_inserted)s, %(error)s,\
                    %(job_date_start)s, %(job_date_end)s, %(job_duration)s)"
        for params in messages:
            self.sql_tools.insert(monitoring_query, params)
