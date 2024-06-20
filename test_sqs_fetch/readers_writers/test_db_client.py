import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError
from sqs_fetch.readers_writers.db_client import DBClient


class TestDBClient(unittest.TestCase):

    def setUp(self):
        self.db_path = 'sqlite:///:memory:'
        self.data = [MagicMock()]

    def test_write_data(self):
        with patch('sqs_fetch.readers_writers.db_client.DBConnection') as db_connection:
            session = MagicMock()
            db_connection.return_value.Session.return_value.__enter__.return_value = session

            model = MagicMock()
            model.__class__.__tablename__ = 'test_table'
            self.data[0].__class__ = model

            db_client = DBClient(self.db_path)
            db_client.write(self.data)

            session.add_all.assert_called_once_with(self.data)
            session.commit.assert_called_once()

