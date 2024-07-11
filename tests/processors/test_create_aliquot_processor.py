import logging
from unittest.mock import MagicMock, patch

import pytest
from lab_share_lib.processing.base_processor import BaseProcessor

from tol_lab_share.processors.create_aliquot_processor import CreateAliquotProcessor

logger = logging.getLogger(__name__)


@pytest.fixture
def basic_publisher():
    return MagicMock()


@pytest.fixture
def schema_registry():
    return MagicMock()


@pytest.fixture
def subject(config, schema_registry, basic_publisher):
    return CreateAliquotProcessor(schema_registry, basic_publisher, config)


@pytest.fixture(autouse=True)
def create_aliquot_in_warehouse_message():
    with patch("tol_lab_share.processors.create_aliquot_processor.CreateAliquotInWarehouseMessage") as cwm:
        yield cwm.return_value


class TestCreateAliquotProcessor:
    def test_is_subclass_of_base_processor(self):
        assert issubclass(CreateAliquotProcessor, BaseProcessor)

    def test_can_be_initialised(self, config, basic_publisher, schema_registry):
        assert CreateAliquotProcessor(schema_registry, basic_publisher, config) is not None

    def test_instantiate_returns_instance(self, config):
        instance = CreateAliquotProcessor.instantiate(MagicMock(), MagicMock(), config)
        assert isinstance(instance, CreateAliquotProcessor)

    def test_instantiate_passes_arguments_to_init(self, config, basic_publisher):
        schema_registry = MagicMock()

        with patch("tol_lab_share.processors.create_aliquot_processor.CreateAliquotProcessor.__init__") as init_mock:
            init_mock.return_value = None
            CreateAliquotProcessor.instantiate(schema_registry, basic_publisher, config)

        init_mock.assert_called_with(schema_registry, basic_publisher, config)

    def test_process_returns_true_for_valid_message(self, subject, valid_traction_to_warehouse_message):
        assert subject.process(valid_traction_to_warehouse_message) is True

    def test_process_called_on_warehouse_messaage(
        self, subject, valid_traction_to_warehouse_message, create_aliquot_in_warehouse_message
    ):
        subject.process(valid_traction_to_warehouse_message)
        create_aliquot_in_warehouse_message.publish.assert_called_once()

    def test_process_populated_warehouse_message_correctly(
        self, subject, valid_traction_to_warehouse_message, create_aliquot_in_warehouse_message
    ):
        """
        Tests the process function that accepts messages from traction and pushes them to the warehouse

            Args:
                valid_traction_to_warehouse_message: Input message from traction service
                create_aliquot_in_warehouse_message: Message sent to the warehouse rabbitmq
        """
        subject.process(valid_traction_to_warehouse_message)

        message = valid_traction_to_warehouse_message.message

        create_aliquot_in_warehouse_message.create_aliquot_message.assert_called_once()
        create_aliquot_message = create_aliquot_in_warehouse_message.create_aliquot_message.return_value

        assert create_aliquot_message.lims == message["limsId"]

        assert create_aliquot_message.aliquot.lims_uuid == message["limsUuid"]
        assert create_aliquot_message.aliquot.id_lims == message["limsId"]
        assert create_aliquot_message.aliquot.aliquot_type == message["aliquotType"]
        assert create_aliquot_message.aliquot.source_type == message["sourceType"]
        assert create_aliquot_message.aliquot.source_barcode == message["sourceBarcode"]
        assert create_aliquot_message.aliquot.sample_name == message["sampleName"]
        assert create_aliquot_message.aliquot.used_by_type == message["usedByType"]
        assert create_aliquot_message.aliquot.used_by_barcode == message["usedByBarcode"]
        assert create_aliquot_message.aliquot.volume == message["volume"]
        assert create_aliquot_message.aliquot.concentration == message["concentration"]

        assert create_aliquot_message.aliquot.created_at == message["createdAt"].strftime("%Y-%m-%dT%H:%M:%SZ")
        assert create_aliquot_message.aliquot.recorded_at == message["recordedAt"].strftime("%Y-%m-%dT%H:%M:%SZ")
        assert create_aliquot_message.aliquot.last_updated == message["recordedAt"].strftime("%Y-%m-%dT%H:%M:%SZ")

    def test_process_called_publish_to_warehouse(
        self, subject, valid_traction_to_warehouse_message, create_aliquot_in_warehouse_message
    ):
        subject.process(valid_traction_to_warehouse_message)

        create_aliquot_in_warehouse_message.publish.assert_called_once()

    def test_process_returns_false_when_mlwh_has_errors(
        self, subject, valid_traction_to_warehouse_message, create_aliquot_in_warehouse_message
    ):
        create_aliquot_in_warehouse_message.errors = ["Error 1", "Error 2"]

        assert not subject.process(valid_traction_to_warehouse_message)

    def test_process_logs_the_error_when_mlwh_has_errors(
        self, subject, valid_traction_to_warehouse_message, create_aliquot_in_warehouse_message, caplog
    ):
        create_aliquot_in_warehouse_message.errors = ["Error 1", "Error 2"]

        subject.process(valid_traction_to_warehouse_message)

        error_records = [r for r in caplog.records if r.levelname == "ERROR"]
        assert len(error_records) == 1

        error_record = error_records[0]
        assert "There was a problem while sending to warehouse" in error_record.message
        assert "['Error 1', 'Error 2']" in error_record.message
