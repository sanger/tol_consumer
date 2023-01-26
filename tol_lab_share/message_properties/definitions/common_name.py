from .message_property import MessageProperty


class CommonName(MessageProperty):
    @property
    def validators(self):
        return [self.check_is_string]
