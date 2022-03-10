from http import HTTPStatus
from flask import current_app as app
from flask_restplus import Resource

import helpers.heartbeat as heartbeat_helper


class Heartbeat(Resource):

    def get(self):
        app.logger.info("Sending Heartbeat by API request..")
        failed, message = heartbeat_helper.send_heartbeat()

        if failed:
            return message, HTTPStatus.OK
        else:
            return "OK", HTTPStatus.OK
