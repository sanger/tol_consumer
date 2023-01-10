from tol_lab_share.message_properties.sanger_sample_id import SangerSampleId


def test_SangerSampleId_check_SangerSampleId_is_string():
    instance = SangerSampleId(None)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = SangerSampleId(1234)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = SangerSampleId([])
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = SangerSampleId("1234")
    assert instance.validate() is True
    assert len(instance.errors) == 0
