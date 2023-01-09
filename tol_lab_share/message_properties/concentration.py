from .message_property import MessageProperty


class Concentration(MessageProperty):
    @property
    def validators(self):
        return [self.check_is_integer]
