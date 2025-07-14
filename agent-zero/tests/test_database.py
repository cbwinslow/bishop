import unittest
import os
from unittest.mock import patch
import sys
sys.path.insert(0, '.')
from core.database import get_db_connection, init_db

class TestDatabase(unittest.TestCase):

    @patch.dict(os.environ, {
        "PG_HOST": "localhost",
        "PG_DATABASE": "test_db",
        "PG_USER": "test_user",
        "PG_PASSWORD": "test_password"
    })
    @patch('psycopg2.connect')
    def test_get_db_connection(self, mock_connect):
        get_db_connection()
        mock_connect.assert_called_with(
            host="localhost",
            database="test_db",
            user="test_user",
            password="test_password"
        )

    @patch('core.database.get_db_connection')
    def test_init_db(self, mock_get_db_connection):
        mock_conn = mock_get_db_connection.return_value
        mock_cursor = mock_conn.cursor.return_value

        init_db()

        self.assertTrue(mock_cursor.execute.called)
        self.assertTrue(mock_conn.commit.called)
        self.assertTrue(mock_cursor.close.called)
        self.assertTrue(mock_conn.close.called)

if __name__ == '__main__':
    unittest.main()
