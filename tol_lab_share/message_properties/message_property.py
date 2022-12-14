class MessageProperty:
    def __init__(self, input):
        self._input = input
        self._errors = []
        self.set_validators()

    def validate(self):
        return all([validator() for validator in self._validators])

    def set_validators(self):
        self._validators = []
