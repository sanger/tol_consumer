# flake8: noqa
import os

from tol_lab_share.config.logging import *
from tol_lab_share.config.rabbit import *

# If we're running in a container, then instead of localhost
# we want host.docker.internal, you can specify this in the
# .env file you use for docker. eg
# LOCALHOST=host.docker.internal
LOCALHOST = os.environ.get("LOCALHOST", "127.0.0.1")
ROOT_PASSWORD = os.environ.get("ROOT_PASSWORD", "")

###
# RedPanda details
###
REDPANDA_BASE_URI = f"http://{os.environ.get('LOCALHOST', '127.0.0.1')}:8081"

TRACTION_URL = f"http://{os.environ.get('LOCALHOST', '127.0.0.1:3100')}/v1/receptions"
TRACTION_QC_URL = f"http://{os.environ.get('LOCALHOST', '127.0.0.1:3100')}/v1/qc_receptions"

EBI_TAXONOMY_URL = "https://www.ebi.ac.uk/ena/taxonomy/rest/tax-id"

# Options: 'json' or 'binary'
SELECTED_ENCODER_FOR_FEEDBACK_MESSAGE = "binary"

# Validate SSL certificate chain when connecting to https
CERTIFICATES_VALIDATION_ENABLED = True
