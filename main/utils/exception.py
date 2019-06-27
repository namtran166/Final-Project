from flask import jsonify


class _Exception(Exception):
    status_code = None
    message = {}

    def __init__(self, message):
        super(Exception).__init__()
        self.message = message

    def messages(self):
        return jsonify(description=self.message), self.status_code


class BadRequestError(_Exception):
    status_code = 400


class UnauthorizedError(_Exception):
    status_code = 401


class ForbiddenError(_Exception):
    status_code = 403


class NotFoundError(_Exception):
    status_code = 404
