from marshmallow import fields, validate

from main.schemas.base import BaseSchema


class UserSchema(BaseSchema):
    id = fields.Integer(dump_only=True)

    username = fields.String(
        required=True,
        unique=True,
        validate=validate.Length(min=6, max=64, error="An username must have between 6-64 characters.")
    )

    password = fields.String(
        required=True,
        load_only=True,
        validate=validate.Length(min=6, max=64, error="A password must have between 6-64 characters.")
    )

    first_name = fields.String(
        validate=validate.Length(max=32, error="First name must be at most 64 characters.")
    )

    last_name = fields.String(
        validate=validate.Length(max=32, error="Last name must be at most 64 characters.")
    )
