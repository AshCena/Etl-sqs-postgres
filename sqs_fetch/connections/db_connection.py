from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBConnection:
    """
    This class is responsible for connecting to the database
    It follows the singleton design pattern.
    """
    _instance = None

    def __new__(cls, path):
        if cls._instance is None:
            cls._instance = super(DBConnection, cls).__new__(cls)
            cls._instance.__init__(path)
            print("Db instance created")
        return cls._instance

    def __init__(self, path):
        self.path = path
        self.engine = create_engine(path)
        self.Session = sessionmaker(bind=self.engine)
