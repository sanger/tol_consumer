from lab_share_lib.rabbit.avro_encoder import AvroEncoder


class CreateLabwareProcessor:
    def __init__(self, schema_registry, basic_publisher, config):
        self._encoder = AvroEncoder(schema_registry, config.RABBITMQ_SUBJECT_CREATE_LABWARE)
        self._basic_publisher = basic_publisher
        self._config = config

    def process(self, message) -> bool:
        pass