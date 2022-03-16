from http import HTTPStatus
from flask_restplus import Resource

from version import VERSION


class Version(Resource):

    def get(self):
        return {"version": VERSION}, HTTPStatus.OK
