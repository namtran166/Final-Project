from marshmallow import fields, validate

from main.schemas.base import BaseSchema


class CategorySchema(BaseSchema):
    name = fields.String(
        required=True,
        unique=True,
        validate=[
            validate.Length(max=256, error="A category name must have must have at most 256 characters.")
        ],
        error_messages={
            "description": "Category name is required."
        }
    )

    description = fields.String()
