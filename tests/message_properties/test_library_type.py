from tol_lab_share.message_properties.library_type import LibraryType


def test_LibraryType_check_LibraryType_is_string():
    instance = LibraryType(None)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = LibraryType(1234)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = LibraryType([])
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = LibraryType("1234")
    assert instance.validate() is True
    assert len(instance.errors) == 0
