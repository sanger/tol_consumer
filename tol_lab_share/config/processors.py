from lab_share_lib.processing.base_processor import BaseProcessor
from tol_lab_share.processors.bioscan_pool_xp_to_traction_processor import BioscanPoolXpToTractionProcessor
from tol_lab_share.processors.create_labware_processor import CreateLabwareProcessor
from tol_lab_share.processors.update_labware_processor import UpdateLabwareProcessor
from tol_lab_share.constants import (
    RABBITMQ_SUBJECT_BIOSCAN_POOL_XP_TO_TRACTION,
    RABBITMQ_SUBJECT_CREATE_LABWARE,
    RABBITMQ_SUBJECT_UPDATE_LABWARE,
)

PROCESSORS: dict[str, BaseProcessor] = {
    RABBITMQ_SUBJECT_BIOSCAN_POOL_XP_TO_TRACTION: BioscanPoolXpToTractionProcessor,
    RABBITMQ_SUBJECT_CREATE_LABWARE: CreateLabwareProcessor,
    RABBITMQ_SUBJECT_UPDATE_LABWARE: UpdateLabwareProcessor,
}
