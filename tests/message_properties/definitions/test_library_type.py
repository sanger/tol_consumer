from tol_lab_share.message_properties.definitions.library_type import LibraryType
from helpers import check_validates_string


def test_LibraryType_check_LibraryType_is_string():
    check_validates_string(LibraryType)
