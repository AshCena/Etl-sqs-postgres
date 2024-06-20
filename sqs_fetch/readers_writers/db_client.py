import logging
from typing import List, Any

from connections.db_connection import DBConnection
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeMeta

from .client_registery import client_registry
from .write_client import WriteClient


class DBClient(WriteClient):

    """
    This class will help instantiate the write client which will help to perform the load step of the ETL.
    """

    def __init__(self, db_path: str):
        self.db_connection = DBConnection(db_path)
        print("db_path ", db_path)

    def write(self, data: List[Any]) -> None:

        if isinstance(data[0].__class__, DeclarativeMeta):
            table_name = data[0].__class__.__tablename__
            print(f"Ensuring table '{table_name}' exists.")
            data[0].__class__.metadata.create_all(self.db_connection.engine)
            print(f"Table '{table_name}' creation checked/completed.")

        if not isinstance(data, list):
            data = [data]

        with self.db_connection.Session() as session:
            try:
                print(f"Adding data to the session")
                session.add_all(data)
                print("Attempting to commit the session.")
                session.commit()
                print(f"Data written successfully to table '{table_name}'.")
            except SQLAlchemyError as e:
                session.rollback()
                print("Exception occurred while writing to the database.")
                print(e)


client_registry.register('postgres', DBClient)
