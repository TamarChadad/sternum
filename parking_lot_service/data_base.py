import pyodbc


class DataBase(object):
    def __init__(self):
        connection_string = ("Driver={SQL Server};"
                             "Server=DESKTOP-FFUJ61T\MSSQLSERVER1;"
                             "Database=ParkingLot;"
                             "Trusted_Connection=yes;")
        self._connection = None
        self._db_cursor = None
        self.connect_to_db(connection_string)

    def connect_to_db(self, connection_string):
        self._connection = pyodbc.connect(connection_string, autocommit=True)
        self._db_cursor = self._connection.cursor()

    def execute_db_cmd(self, cmd):
        return self._db_cursor.execute(cmd)

    def disconnect(self):
        self._db_cursor.close()
        self._connection.close()
