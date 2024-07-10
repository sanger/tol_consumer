from unittest.mock import MagicMock, patch

import pytest
from lab_share_lib.processing.base_processor import BaseProcessor
from tol_lab_share.processors.create_aliquot_processor import CreateAliquotProcessor


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
