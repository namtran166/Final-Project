from marshmallow import Schema, pre_load

from main.utils.exception import BadRequestError


class BaseSchema(Schema):
    def handle_error(self, error, data):
        return_message = ""
        missing_dict = ["Missing data for required field."]

        failed_validation_messages = [
            error.messages[key][0] for key in error.messages if error.messages[key] != missing_dict
        ]
        for error_message in failed_validation_messages:
            return_message += error_message + " "

        missing_fields = [key for key in error.messages if error.messages[key] == missing_dict]
        if missing_fields:
            return_message += "Missing data for required field: "
            for field in missing_fields:
                return_message += field + " "

        return_message = return_message[:-1]
        if missing_fields:
            return_message += "."
        raise BadRequestError(return_message)


class BaseUserSchema(BaseSchema):
    @pre_load
    def pre_process_value(self, data):
        if "username" in data:
            data["username"] = data["username"].strip()
        if "password" in data:
            data["password"] = data["password"].strip()
        return data
