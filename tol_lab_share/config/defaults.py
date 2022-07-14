# flake8: noqa
import os

from tol_lab_share.config.processors import *
from tol_lab_share.config.logging import *

# If we're running in a container, then instead of localhost
# we want host.docker.internal, you can specify this in the
# .env file you use for docker. eg
# LOCALHOST=host.docker.internal
LOCALHOST = os.environ.get("LOCALHOST", "127.0.0.1")
ROOT_PASSWORD = os.environ.get("ROOT_PASSWORD", "")


###
# RabbitMQ details
###
RABBITMQ_HOST = os.environ.get("LOCALHOST", "127.0.0.1")
RABBITMQ_SSL = False
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = "admin"
RABBITMQ_PASSWORD = "development"
RABBITMQ_VHOST = "tol"
RABBITMQ_CRUD_QUEUE = "tol.crud-labware"
RABBITMQ_FEEDBACK_EXCHANGE = "psd.tol"

###
# RedPanda details
###
REDPANDA_BASE_URI = f"http://{os.environ.get('LOCALHOST', '127.0.0.1')}:8081"
REDPANDA_API_KEY = ""


###
# slack details
###
SLACK_API_TOKEN = ""
SLACK_CHANNEL_ID = ""

