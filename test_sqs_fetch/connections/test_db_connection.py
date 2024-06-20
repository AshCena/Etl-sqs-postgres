import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError
from sqs_fetch.connections.db_connection import DBConnection


class TestDBConnection(unittest.TestCase):

    def setUp(self):
        self.db_path = 'sqlite:///:memory:'

    def test_duplicate_instance_creation(self):
        with patch('sqs_fetch.connections.db_connection.create_engine') as create_engine:
            create_engine.return_value = MagicMock()
            instance_1 = DBConnection(self.db_path)
            instance_2 = DBConnection(self.db_path)
            self.assertIs(instance_1, instance_2)

    def test_database_connection(self):
        with patch('sqs_fetch.connections.db_connection.create_engine') as create_engine:
            engine = MagicMock()
            connection = MagicMock()

            engine.connect.return_value = connection
            create_engine.return_value = engine

            try:
                db_connection = DBConnection(self.db_path)
                connection = db_connection.engine.connect()
                connection.close()
                success = True
            except SQLAlchemyError:
                success = False
            self.assertTrue(success)

    def test_session_creation(self):
        with patch('sqs_fetch.connections.db_connection.create_engine') as create_engine, \
                patch('sqs_fetch.connections.db_connection.sessionmaker') as sessionmaker:
            engine = MagicMock()
            session = MagicMock()
            create_engine.return_value = engine
            sessionmaker.return_value = MagicMock(return_value=session)

            try:
                db_connection = DBConnection(self.db_path)
                session = db_connection.Session()
                session.execute('SELECT 9')
                session.close()
                success = True
            except SQLAlchemyError:
                success = False
            self.assertTrue(success)

