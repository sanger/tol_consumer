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
RABBITMQ_USERNAME = os.environ.get("RABBITMQ_USER", "admin")
RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD", "development")
RABBITMQ_VHOST = "tol"
RABBITMQ_CRUD_QUEUE = "tol.crud-operations"
RABBITMQ_FEEDBACK_EXCHANGE = "psd.tol"

###
# RedPanda details
###
REDPANDA_BASE_URI = f"http://{os.environ.get('LOCALHOST', '127.0.0.1')}:8081"
REDPANDA_API_KEY = ""


RABBITMQ_PUBLISH_RETRY_DELAY = 5
RABBITMQ_PUBLISH_RETRIES = 36  # 3 minutes of retries

TRACTION_URL = f"https://{os.environ.get('LOCALHOST', '127.0.0.1')}:3000/v1/receptions"

EBI_TAXONOMY_URL = "https://www.ebi.ac.uk/ena/taxonomy/rest/tax-id"
