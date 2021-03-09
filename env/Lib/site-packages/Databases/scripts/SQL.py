"""SQL database functionality"""
import mysql.connector

class SQL:
    """SQL database class"""

    def __init__(self, data):
        """SQL database constructor"""
        self.type = data['type']
        self.user = data['user']
        self.password = data['password']
        self.host = data['host']
        self.schema = data['schema']

    def connect(self):
        """SQL database connecting method"""
        connection = mysql.connector.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.schema,
            buffered=True
        )
        return connection

    def get(self, query, all=False):
        """SQL database SELECT querries"""

        # Single values
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query)

        if all: data = cursor.fetchall()
        else: data = cursor.fetchone()

        connection.close()

        return data


        # All values

    def write(self, query):
        """SQL database INSERT querries"""

        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()

    def execute(self, query):
        """SQL database other querries"""

        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()
