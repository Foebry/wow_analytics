"""SQL database testing functionality"""

import unittest
import mysql.connector
from Databases.scripts.SQL import SQL



class TestResult(unittest.TestResult):
    """defining fail result of tests"""
    def addFailure(self, test, err):
        errors.append(f"Expected {self.expected}, got {self.actual}")



class SQLTest(unittest.TestCase):

    def test_init(self):
        """testing __init__ functionality"""

        # testing attributes
        self.assertEqual('MySQL', database.type)
        self.assertEqual('Network', database.user)
        self.assertEqual('Sander', database.password)
        self.assertEqual('localhost', database.host)
        self.assertEqual('wow', database.schema)

        return database


    def test_connect(self):
        """testing connect functionality"""

        # connecting to database
        connection = database.connect()

        # testing functionality
        self.assertEqual(mysql.connector.connection.MySQLConnection, type(connection))


    def test_get(self):
        """testing SELECT querries functionality"""

        # single value
        values = ('*', 'items', 'id', 0)
        query = "SELECT %s FROM %s where %s = %s" %values
        data = database.get(query)

        # testing functionality
        self.assertEqual(11, len(data))
        self.assertEqual(0, data[0])
        self.assertEqual(0, data[1])
        self.assertEqual(0, data[2])
        self.assertEqual(0, data[3])
        self.assertEqual('TEST', data[4])
        self.assertEqual('TEST', data[5])
        self.assertEqual(0, data[6])
        self.assertEqual(0, data[7])
        self.assertEqual('TEST', data[8])
        self.assertEqual('TEST', data[9])
        self.assertEqual(0.0000, data[10])


        # testing for multiple values
        values = ('*', 'items')
        query = "SELECT %s from %s" %values
        data = database.get(query, True)

        # testing functionality
        temp = data[0]
        self.assertEqual(3, len(data))
        self.assertEqual(0, temp[0])
        self.assertEqual(0, temp[1])
        self.assertEqual(0, temp[2])
        self.assertEqual(0, temp[3])
        self.assertEqual('TEST', temp[4])
        self.assertEqual('TEST', temp[5])
        self.assertEqual(0, temp[6])
        self.assertEqual(0, temp[7])
        self.assertEqual('TEST', temp[8])
        self.assertEqual('TEST', temp[9])
        self.assertEqual(0.0000, temp[10])

        temp = data[1]
        self.assertEqual(1, temp[0])
        self.assertEqual(0, temp[1])
        self.assertEqual(0, temp[2])
        self.assertEqual(0, temp[3])
        self.assertEqual('TEST', temp[4])
        self.assertEqual('TEST', temp[5])
        self.assertEqual(0, temp[6])
        self.assertEqual(0, temp[7])
        self.assertEqual('TEST', temp[8])
        self.assertEqual('TEST', temp[9])
        self.assertEqual(0.0000, temp[10])


    def test_write(self):
        """testing INSERT querries functionality"""

        # writing into database
        values = ('classes', 'id', 'name', 0, '"TEST"')
        query = "INSERT into %s (%s, %s) VALUES(%s, %s)" %values
        database.write(query)

        # selecting from database
        values = ('classes')
        query = "SELECT * from %s " %values
        data = database.get(query)

        # testing functionality
        self.assertEqual(2, len(data))
        self.assertEqual(0, data[0])
        self.assertEqual('TEST', data[1])


    def test_execute(self):
        """testing other querries functionality"""

        # test for UPDATE
        # altering data
        values = ('classes', 'id', 5, 'id', 0)
        query = "UPDATE %s SET %s=%s where %s=%s" %values
        database.execute(query)

        # selecting from database
        values = ('classes')
        query = "SELECT * from %s " %values
        data = database.get(query)

        # testing functionality
        self.assertEqual(2, len(data))
        self.assertEqual(5, data[0])
        self.assertEqual('TEST', data[1])


if __name__ == '__main__':
    # creating data
    data = {
        'type': 'MySQL',
        'user': 'Network',
        'password': 'Sander',
        'host': 'localhost',
        'schema': 'wow'
    }
    # creating database
    database = SQL(data)
    # testing functionalities
    unittest.main()
