import mysql.connector
from util.property_util import PropertyUtil

class DBConnection:
    connection = None

    @staticmethod
    def get_connection():
        if DBConnection.connection is None:
            props = PropertyUtil.get_property_string()
            DBConnection.connection = mysql.connector.connect(
                host=props['host'],
                port=props['port'],
                user=props['user'],
                password=props['password'],
                database=props['database']
            )
        return DBConnection.connection
