from .message_property import MessageProperty


class Volume(MessageProperty):
    @property
    def validators(self):
        return [self.check_is_integer]
