from marshmallow import fields, validate

from main.schemas.base import BaseSchema


class ItemSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, error="An item name must have must have at least 1 character.")
    )

    description = fields.String()

    category_id = fields.Integer(required=True, dump_only=True)

    user_id = fields.Integer(required=True, dump_only=True)

    created = fields.DateTime(dump_only=True)

    updated = fields.DateTime(dump_only=True)
