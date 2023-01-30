from .message_property import MessageProperty


class PublicName(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid public name string provided by another
    MessageProperty.
    The public name has to be a string.
    Eg: 'public_name_1'
    """

    @property
    def validators(self):
        return [self.check_is_string]
