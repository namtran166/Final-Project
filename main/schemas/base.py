from marshmallow import Schema, fields


class BaseSchema(Schema):
    id = fields.Integer(dump_only=True)

    date_created = fields.DateTime(dump_only=True)

    date_modified = fields.DateTime(dump_only=True)
