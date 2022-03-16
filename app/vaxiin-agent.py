import os
from flask import Flask
from flask_restplus import Api
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

from config import configure_app, configure_logging
import helpers.heartbeat as heartbeat_helper
from routes.heartbeat import Heartbeat
from routes.version import Version


default_path = '/v1/agent'


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Heartbeat, default_path + '/heartbeat')
    api.add_resource(Version, '/version')

    return app


def create_heartbeat_scheduler(app):
    # Make sure we run just once in debug mode
    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        sched = BackgroundScheduler()
        sched_job = sched.add_job(trigger="interval", func=heartbeat_helper.send_interval_heartbeat, args=[app],
                                  minutes=app.config.get('heartbeat_interval'),
                                  next_run_time=(datetime.now() + timedelta(seconds=10)))
        sched.start()
        app.sched_job = sched_job


if __name__ == '__main__':
    configure_logging()
    app = create_app()
    configure_app(app)
    create_heartbeat_scheduler(app)
    app.run(port=app.config['port'], host=app.config['host'])
