from tol_lab_share.message_properties.donor_id import DonorId


def test_DonorId_check_DonorId_is_string():
    instance = DonorId(None)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = DonorId(1234)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = DonorId([])
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = DonorId("1234")
    assert instance.validate() is True
    assert len(instance.errors) == 0
