from sqlalchemy import Column, String

from main.database import db
from main.models.base import BaseModel


class CategoryModel(BaseModel):
    __tablename__ = 'category'

    name = Column(String(256), nullable=False, unique=True)
    description = Column(String)

    # Relationship
    items = db.relationship('ItemModel', lazy=True)

    def __init__(self, *args, **kwargs):
        super(CategoryModel, self).__init__(*args, **kwargs)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_all_categories(cls):
        return cls.query.all()
