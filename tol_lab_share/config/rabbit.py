import os
from lab_share_lib.config.rabbit_config import RabbitConfig
from lab_share_lib.config.rabbit_server_details import RabbitServerDetails

from tol_lab_share.constants import (
    RABBITMQ_SUBJECT_BIOSCAN_POOL_XP_TO_TRACTION,
    RABBITMQ_SUBJECT_CREATE_LABWARE,
    RABBITMQ_SUBJECT_UPDATE_LABWARE,
)
from tol_lab_share.processors.bioscan_pool_xp_to_traction_processor import BioscanPoolXpToTractionProcessor
from tol_lab_share.processors.create_labware_processor import CreateLabwareProcessor
from tol_lab_share.processors.update_labware_processor import UpdateLabwareProcessor

RABBIT_SERVER_DETAILS = RabbitServerDetails(
    uses_ssl=False,
    host=os.environ.get("LOCALHOST", "127.0.0.1"),
    port=5672,
    username=os.environ.get("RABBITMQ_USER", "admin"),
    password=os.environ.get("RABBITMQ_PASSWORD", "development"),
    vhost="tol",
)

RABBITMQ_SERVERS = [
    RabbitConfig(
        consumer_details=RABBIT_SERVER_DETAILS,
        consumed_queue="tls.poolxp-export-to-traction",
        processors={
            RABBITMQ_SUBJECT_BIOSCAN_POOL_XP_TO_TRACTION: BioscanPoolXpToTractionProcessor,
        },
        publisher_details=RABBIT_SERVER_DETAILS,
    ),
    RabbitConfig(
        consumer_details=RABBIT_SERVER_DETAILS,
        consumed_queue="tol.crud-operations",
        processors={
            RABBITMQ_SUBJECT_CREATE_LABWARE: CreateLabwareProcessor,
            RABBITMQ_SUBJECT_UPDATE_LABWARE: UpdateLabwareProcessor,
        },
        publisher_details=RABBIT_SERVER_DETAILS,
    ),
]

RABBITMQ_PUBLISH_RETRY_DELAY = 5
RABBITMQ_PUBLISH_RETRIES = 36  # 3 minutes of retries
