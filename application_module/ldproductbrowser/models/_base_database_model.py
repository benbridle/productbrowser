import os
import sqlite3


class _BaseDatabaseModel:
    """
    Base class for all database models. Implements common functionality to do
    with loading and querying the database.
    """

    def __init__(self, database_file_path):
        if not os.path.isfile(database_file_path):
            raise FileNotFoundError(f"No database at '{database_file_path}'")
        self.db = sqlite3.connect(database_file_path)

    def execute(self, query, parameters=None):
        if parameters and not isinstance(parameters, (tuple, list)):
            raise TypeError("parameters must be a tuple or a list")
        parameters = parameters or []
        cursor = self.db.cursor()
        cursor.execute(query, parameters)
        return cursor
