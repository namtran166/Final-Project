from sqlalchemy import Column, String

from main.models.base import BaseModel


class UserModel(BaseModel):
    __tablename__ = 'user'

    username = Column(String(64), nullable=False, unique=True)
    hashed_password = Column(String(128), nullable=False)
    first_name = Column(String(32))
    last_name = Column(String(32))

    def __init__(self, *args, **kwargs):
        super(UserModel, self).__init__(*args, **kwargs)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
