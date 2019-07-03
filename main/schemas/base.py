from marshmallow import Schema, pre_load

from main.utils.exception import BadRequestError


class BaseSchema(Schema):
    def handle_error(self, error, data):
        """
        This method will handle the Validation Error messages raise by our schemas
        :param error: List of Validation Errors that were raised by our schemas
        :return: A customized error message for all the Validation Errors we have
        """
        return_message = ''
        missing_message = ['Missing data for required field.']

        # List of error messages by failing the validate function
        validate_errors = [
            error.messages[key][0] for key in error.messages if error.messages[key] != missing_message
        ]
        for error_message in validate_errors:
            return_message += error_message + ' '

        # List of error messages by missing required fields
        missing_errors = [key for key in error.messages if error.messages[key] == missing_message]
        if missing_errors:
            return_message += 'Missing data for required field(s): '
            for missing_field in missing_errors:
                return_message += missing_field + ' '

        # Replace extra space at the end and add a comma if needed
        return_message = return_message[:-1]
        if missing_errors:
            return_message += '.'
        raise BadRequestError(return_message)


class StripSchema(Schema):
    @pre_load
    def pre_load(self, data):
        for key, value in data.items():
            if type(value) is str:
                data[key] = data[key].strip()
