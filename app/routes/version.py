from http import HTTPStatus
from flask_restplus import Resource, Namespace

from version import VERSION

ns = Namespace('Version', description='Get agent version')


@ns.route('/')
class Version(Resource):

    @ns.doc('get agent version')
    @ns.response(HTTPStatus.OK, 'Success')
    def get(self):
        return {"version": VERSION}, HTTPStatus.OK
