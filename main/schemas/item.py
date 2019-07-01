from marshmallow import fields, validate

from main.schemas.base import BaseSchema
from main.schemas.user import UserSchema


class ItemSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=256, error="An item name must have between 1-256 characters.")
    )

    description = fields.String(
        validate=validate.Length(max=1024, error="An item description must have at most 1024 characters.")
    )

    category_id = fields.Integer(required=True, dump_only=True)

    user = fields.Nested(UserSchema, only=("id", "username"))

    created = fields.DateTime(dump_only=True)

    updated = fields.DateTime(dump_only=True)
