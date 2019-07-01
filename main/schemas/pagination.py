from marshmallow import fields, validate

from main.schemas.base import BaseSchema
from main.schemas.item import ItemSchema


class PaginationSchema(BaseSchema):
    page = fields.Integer(
        validate=validate.Range(min=1, error="Requested page must be positive.")
    )

    per_page = fields.Integer(
        validate=validate.Range(min=1, max=100, error="One page can only display between 1-100 items.")
    )

    total_items = fields.Integer(dump_only=True)

    total_pages = fields.Integer(dump_only=True)

    items = fields.Nested(ItemSchema, many=True, only=("id", "name", "description", "user"))
