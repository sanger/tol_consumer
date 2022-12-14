from .message_property import MessageProperty
from uuid import UUID

class Uuid(MessageProperty):
    def set_validators(self):
        self._validators = [self.check_is_binary, self.check_is_uuid]

    def check_is_binary(self):
        try:
            self._input.decode('utf-8')
        except AttributeError:
            self._errors.append('The string for uuid is not a binary')
            return False
        return True

    def check_is_uuid(self):
        try:
            str_rep = self._input.decode('utf-8')
            uuid_obj = UUID(str_rep, version=4)
        except ValueError:
            self._errors.append('The string is not a uuid')
            return False
        except AttributeError:
            self._errors.append('The string is not a binary')
            return False
        return str(uuid_obj) == str(str_rep)

