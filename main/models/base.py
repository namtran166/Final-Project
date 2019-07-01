import datetime

from sqlalchemy import Column, DateTime, Integer

from main.database import db
from main.utils.exception import DatabaseError


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, default=datetime.datetime.now)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(
                "Unexpected Error trying to save to the database. "
                "Error message: {}".format(str(e))
            )

    def delete_from_db(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise DatabaseError(
                "Unexpected Error trying to delete to the database. "
                "Error message: {}".format(str(e))
            )

    def update_to_db(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save_to_db()
