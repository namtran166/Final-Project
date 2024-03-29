from sqlalchemy import Column, String

from main.database import db
from main.models.base import BaseModel


class CategoryModel(BaseModel):
    __tablename__ = 'category'

    name = Column(String(256), nullable=False, unique=True)
    description = Column(String(1024))

    # Relationship
    items = db.relationship('ItemModel', lazy=True)

    def __init__(self, *args, **kwargs):
        super(CategoryModel, self).__init__(*args, **kwargs)
