from tol_lab_share.messages.properties.complex import CountryOfOrigin
from tol_lab_share.messages.properties.simple import Value


class TestCountryOfOrigin:
    def test_validators_behave_correctly(self):
        instance = CountryOfOrigin(Value(None))
        assert instance.validate() is False
        assert len(instance.errors) > 0

        instance = CountryOfOrigin(Value("1234"))
        assert instance.validate() is False
        assert len(instance.errors) > 0

        instance = CountryOfOrigin(Value([]))
        assert instance.validate() is False
        assert len(instance.errors) > 0

        instance = CountryOfOrigin(Value(1234))
        assert instance.validate() is False
        assert len(instance.errors) > 0

        instance = CountryOfOrigin(Value("Testing"))
        assert instance.validate() is False
        assert len(instance.errors) > 0

        instance = CountryOfOrigin(Value("UNITED KINGDOM"))
        assert instance.validate() is True
        assert len(instance.errors) == 0
