import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from main.database import db
from main.models.base import BaseModel


class ItemModel(BaseModel):
    __tablename__ = 'item'

    name = Column(String(256), nullable=False)
    description = Column(String(1024))
    updated = Column(DateTime,
                     default=datetime.datetime.now,
                     onupdate=datetime.datetime.now)

    # Foreign keys
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)

    # Relationships
    user = db.relationship('UserModel', lazy=True)
    category = db.relationship('CategoryModel', lazy=True)

    def __init__(self, *args, **kwargs):
        super(ItemModel, self).__init__(*args, **kwargs)
