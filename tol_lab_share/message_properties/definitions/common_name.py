from .message_property import MessageProperty


class CommonName(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid common name string provided by another
    MessageProperty.
    The common name has to be a string.
    Eg: 'test'
    """

    @property
    def validators(self):
        return [self.check_is_string]
