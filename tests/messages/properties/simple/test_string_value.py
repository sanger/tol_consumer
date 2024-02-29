from tol_lab_share.messages.properties.simple import StringValue
from tests.messages.properties.helpers import check_validates_string


class TestStringValue:
    def test_validates_strings(self):
        check_validates_string(StringValue)
