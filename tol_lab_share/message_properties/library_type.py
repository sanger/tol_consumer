from .message_property import MessageProperty


class LibraryType(MessageProperty):
    @property
    def validators(self):
        return [self.check_is_string]
