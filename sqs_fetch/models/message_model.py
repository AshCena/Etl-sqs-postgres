from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Message(Base):
    """
    This class represents a message in the SQS queue.
    """

    __tablename__ = 'user_logins'
    user_id = Column(String(128), primary_key=True)
    device_type = Column(String(32))
    masked_ip = Column(String(256))
    masked_device_id = Column(String(256))
    locale = Column(String(32))
    app_version = Column(Integer)
    create_date = Column(Date)

    @classmethod
    def from_dict(cls, data):
        return cls(**data) if data is not None else None
