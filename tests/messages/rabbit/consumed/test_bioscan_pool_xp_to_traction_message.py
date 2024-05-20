from tol_lab_share import error_codes
from tol_lab_share.messages.rabbit.consumed.bioscan_pool_xp_to_traction_message import BioscanPoolXpToTractionMessage
from tol_lab_share.messages.traction.reception_message import TractionReceptionMessage


def check_error_is_present(message, error_code, field):
    assert any(
        [((x.type_id == error_code.type_id) and (x.field == field)) for x in message.errors]
    ), f"Error type '{error_code.type_id}' for field '{field}' not found among {message.errors}"


class TestBioscanPoolXpToTractionMessage:
    def test_validates_true_when_valid(self, valid_bioscan_pool_xp_to_traction_message):
        subject = BioscanPoolXpToTractionMessage(valid_bioscan_pool_xp_to_traction_message)
        assert subject.validate() is True
        assert len(subject.errors) == 0

    def test_validates_false_when_invalid(self, invalid_bioscan_pool_xp_to_traction_message):
        instance = BioscanPoolXpToTractionMessage(invalid_bioscan_pool_xp_to_traction_message)
        assert instance.validate() is False

        check_error_is_present(instance, error_codes.ERROR_2_UUID_NOT_RIGHT_FORMAT, "uuid")
        check_error_is_present(instance, error_codes.ERROR_9_INVALID_INPUT, "tube_barcode")
        check_error_is_present(instance, error_codes.ERROR_5_NOT_FLOAT, "volume")
        check_error_is_present(instance, error_codes.ERROR_9_INVALID_INPUT, "concentration")
        check_error_is_present(instance, error_codes.ERROR_2_NOT_STRING, "box_barcode")
        check_error_is_present(instance, error_codes.ERROR_3_NOT_INTEGER, "insert_size")
        check_error_is_present(instance, error_codes.ERROR_2_NOT_STRING, "cost_code")
        check_error_is_present(instance, error_codes.ERROR_2_NOT_STRING, "library_type")
        check_error_is_present(instance, error_codes.ERROR_2_UUID_NOT_RIGHT_FORMAT, "study_uuid")
        check_error_is_present(instance, error_codes.ERROR_9_INVALID_INPUT, "name")
        check_error_is_present(instance, error_codes.ERROR_1_UUID_NOT_BINARY, "uuid")
        check_error_is_present(instance, error_codes.ERROR_2_UUID_NOT_RIGHT_FORMAT, "uuid")
        check_error_is_present(instance, error_codes.ERROR_2_NOT_STRING, "species_name")

        assert len(instance.errors) == 13

    def test_add_to_message_property_for_traction_reception_message(self, valid_bioscan_pool_xp_to_traction_message):
        instance = BioscanPoolXpToTractionMessage(valid_bioscan_pool_xp_to_traction_message)
        message = TractionReceptionMessage()

        # Sanity check
        assert len(message._requests) == 0

        instance.add_to_message_property(message)

        assert len(message._requests) == 1

        request = message._requests[0]
        assert request.container_type == "tubes"
        assert request.container_barcode == valid_bioscan_pool_xp_to_traction_message.message["tubeBarcode"]

        # Check that more than the above properties were populated by the method under test.
        assert len([r for r in vars(request) if vars(request)[r] is not None]) > 2
