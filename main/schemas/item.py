from marshmallow import fields, validate

from main.schemas.base import BaseSchema


class ItemSchema(BaseSchema):
    name = fields.String(
        required=True,
        validate=[
            validate.Length(max=256, error="An item name must have must have at most 256 characters.")
        ],
        error_messages={
            "description": "Item name is required."
        }
    )

    description = fields.String()

    category_id = fields.Integer(
        required=True,
        error_messages={
            "description": "Category id is required."
        }
    )

    user_id = fields.Integer(
        required=True,
        error_messages={
            "description": "User id is required."
        }
    )
