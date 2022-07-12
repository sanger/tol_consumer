from typing import Dict, cast

from lab_share_lib.processing.base_processor import BaseProcessor
#from lab_share_lib.processing.create_plate_processor import CreatePlateProcessor
#from lab_share_lib.processing.update_sample_processor import UpdateSampleProcessor


RABBITMQ_SUBJECT_CREATE_PLATE = "create-plate-map"
RABBITMQ_SUBJECT_UPDATE_SAMPLE = "update-plate-map-sample"

PROCESSORS: Dict[str, BaseProcessor] = {
    #RABBITMQ_SUBJECT_CREATE_PLATE: cast(BaseProcessor, CreatePlateProcessor),
    #RABBITMQ_SUBJECT_UPDATE_SAMPLE: cast(BaseProcessor, UpdateSampleProcessor),
}
