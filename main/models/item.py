import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from main.database import db
from main.models.base import BaseModel


class ItemModel(BaseModel):
    __tablename__ = 'item'

    name = Column(String(65000), nullable=False)
    description = Column(String(65000))
    created = Column(DateTime,
                     default=datetime.datetime.now())
    updated = Column(DateTime,
                     default=datetime.datetime.now(),
                     onupdate=datetime.datetime.now())

    # Foreign keys
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)

    # Relationships
    user = db.relationship('UserModel', lazy=True)
    category = db.relationship('CategoryModel', lazy=True)

    def __init__(self, *args, **kwargs):
        super(ItemModel, self).__init__(*args, **kwargs)

    @classmethod
    def get_items_by_category_id(cls, category_id):
        return cls.query.filter_by(category_id=category_id).all()

    @classmethod
    def duplicate_item_exists(cls, name, category_id, user_id):
        return cls.query.filter_by(name=name, category_id=category_id, user_id=user_id).count() != 0
