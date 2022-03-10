import os
import sys
import yaml
from logging.config import dictConfig


class BaseConfig(object):
    AGENT_VERSION = '0.1'


class Development(BaseConfig):
    DEBUG = True
    TESTING = False
    ENV = 'dev'


class Production(BaseConfig):
    DEBUG = False
    TESTING = False
    ENV = 'prod'


config = {
    'development': 'config.Development',
    'production': 'config.Production'
}


def configure_app(app):
    app.config.from_object(config[os.getenv('APP_ENV', 'production')])
    add_agent_config(app)


def add_agent_config(app):
    config_file_location = os.getenv('AGENT_CONFIG_PATH', '/etc/vaxiin-agent-config/config.yaml')
    try:
        with open(config_file_location) as file:
            agent_config = yaml.full_load(file)
    except FileNotFoundError:
        print(f"Failed to find configuration file at '{config_file_location}', exitting...")
        sys.exit(2)

    app.config['host'] = agent_config.get('host', '127.0.0.1')
    app.config['port'] = agent_config.get('port', 4000)
    app.config['vaxiin_server_url'] = agent_config.get('vaxiin_server_url', "http://localhost:5000")
    app.config['heartbeat_interval'] = agent_config.get('heartbeat_interval', 60)
    missing_keys = ["uid", "ipmi_ip", "model"] - agent_config.keys()
    if missing_keys:
        print(f"Failed to find required configuration keys '{', '.join(missing_keys)}', exitting...")
        sys.exit(3)

    app.config['uid'] = agent_config.get('uid')
    app.config['ipmi_ip'] = agent_config.get('ipmi_ip')
    app.config['model'] = agent_config.get('model')
    app.config['creds_name'] = app.config.get('creds_name')


def configure_logging():
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': os.getenv('APP_LOG_LEVEL', 'INFO'),
            'handlers': ['wsgi']
        }
    })
