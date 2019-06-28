from marshmallow import fields, validate

from main.schemas.base import BaseSchema


class CategorySchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(
        required=True,
        unique=True,
        validate=validate.Length(min=1, error="A category name must have must have at most 256 characters.")
    )

    description = fields.String()
