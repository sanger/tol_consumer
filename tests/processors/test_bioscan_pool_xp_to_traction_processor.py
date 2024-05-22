from unittest.mock import MagicMock, patch
import pytest

from lab_share_lib.processing.base_processor import BaseProcessor
from tol_lab_share.processors.bioscan_pool_xp_to_traction_processor import BioscanPoolXpToTractionProcessor


@pytest.fixture
def subject(config):
    return BioscanPoolXpToTractionProcessor(config)


@pytest.fixture(autouse=True)
def traction_reception_message():
    with patch("tol_lab_share.processors.bioscan_pool_xp_to_traction_processor.TractionReceptionMessage") as trm:
        yield trm.return_value


class TestBioscanPoolXpToTractionProcessor:
    """Tests for the BioscanPoolXpToTractionProcessor class.
    Note, however, that the tests of the process method are more like integration tests, checking that the entire
    process works. Those tests are therefore not mocking out the dependencies apart from the TractionReceptionMessage so
    that we can check the correct message would go to Traction.
    """

    def test_is_subclass_of_base_processor(self):
        assert issubclass(BioscanPoolXpToTractionProcessor, BaseProcessor)

    def test_can_be_initialised(self, config):
        assert BioscanPoolXpToTractionProcessor(config) is not None

    def test_instantiate_returns_instance(self, config):
        instance = BioscanPoolXpToTractionProcessor.instantiate(MagicMock(), MagicMock(), config)
        assert isinstance(instance, BioscanPoolXpToTractionProcessor)

    def test_instantiate_passes_arguments_to_init(self, config):
        with patch(
            "tol_lab_share.processors.bioscan_pool_xp_to_traction_processor.BioscanPoolXpToTractionProcessor.__init__"
        ) as init_mock:
            init_mock.return_value = None
            BioscanPoolXpToTractionProcessor.instantiate(MagicMock(), MagicMock(), config)

        init_mock.assert_called_with(config)

    def test_process_returns_true_for_valid_message(self, subject, valid_bioscan_pool_xp_to_traction_message):
        assert subject.process(valid_bioscan_pool_xp_to_traction_message) is True

    def test_process_populated_traction_message_correctly(
        self, subject, valid_bioscan_pool_xp_to_traction_message, traction_reception_message
    ):
        subject.process(valid_bioscan_pool_xp_to_traction_message)

        message = valid_bioscan_pool_xp_to_traction_message.message

        traction_reception_message.create_request.assert_called_once()
        request = traction_reception_message.create_request.return_value
        assert request.container_type == "tubes"
        assert request.container_barcode == message["tubeBarcode"]

        library_section = message["library"]
        assert request.library_volume == library_section["volume"]
        assert request.library_concentration == library_section["concentration"]
        assert request.template_prep_kit_box_barcode == library_section["boxBarcode"]
        assert request.library_insert_size == library_section["insertSize"]

        request_section = message["request"]
        assert request.cost_code == request_section["costCode"]
        assert request.genome_size == request_section["genomeSize"]
        assert request.library_type == request_section["libraryType"]
        assert request.study_uuid == request_section["studyUuid"].decode()

        sample_section = message["sample"]
        assert request.sample_name == sample_section["sampleName"]
        assert request.sample_uuid == sample_section["sampleUuid"].decode()
        assert request.species == sample_section["speciesName"]

    def test_process_called_send_on_traction_message(
        self, subject, valid_bioscan_pool_xp_to_traction_message, traction_reception_message
    ):
        subject.process(valid_bioscan_pool_xp_to_traction_message)

        traction_reception_message.send.assert_called_once()

    def test_process_returns_false_when_traction_has_errors(
        self, subject, valid_bioscan_pool_xp_to_traction_message, traction_reception_message
    ):
        traction_reception_message.errors = ["Error 1", "Error 2"]

        assert subject.process(valid_bioscan_pool_xp_to_traction_message) is False

    def test_process_logs_the_error_when_traction_has_errors(
        self, subject, valid_bioscan_pool_xp_to_traction_message, traction_reception_message, caplog
    ):
        traction_reception_message.errors = ["Error 1", "Error 2"]

        subject.process(valid_bioscan_pool_xp_to_traction_message)

        error_records = [r for r in caplog.records if r.levelname == "ERROR"]
        assert len(error_records) == 1

        error_record = error_records[0]
        assert "There was a problem while sending to traction" in error_record.message
        assert "['Error 1', 'Error 2']" in error_record.message

    def test_process_returns_false_when_validation_fails(self, subject, invalid_bioscan_pool_xp_to_traction_message):
        assert subject.process(invalid_bioscan_pool_xp_to_traction_message) is False

    def test_process_logs_the_error_when_validation_fails(
        self, subject, invalid_bioscan_pool_xp_to_traction_message, caplog
    ):
        subject.process(invalid_bioscan_pool_xp_to_traction_message)

        error_records = [r for r in caplog.records if r.levelname == "ERROR"]
        assert len(error_records) == 4
        assert 'Uuid has wrong format, text: "input: 01234-56789ab-cdef-0123-456789abcdef"' in [r.message for r in error_records]
        assert 'Uuid has wrong format, text: "input: 456789ab-cdef-0123-456789ab-cdef0123"' in [r.message for r in error_records]
        assert 'Uuid has wrong format, text: "input: 89abcdef-0123-456789ab-cdef0123-4567"' in [r.message for r in error_records]
        assert any([r.message.startswith("There was a problem while validating the input message") for r in error_records])
