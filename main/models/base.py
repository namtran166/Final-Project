import datetime

from sqlalchemy import Column, Integer, DateTime

from main.database import db


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(DateTime,
                          default=datetime.datetime.now())
    date_modified = Column(DateTime,
                           default=datetime.datetime.now(),
                           onupdate=datetime.datetime.now())

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_to_db(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
