from .message_property import MessageProperty


class DonorId(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid donor id string provided by another
    MessageProperty.
    The donor id has to be a string.
    Eg: 'donor'
    """

    @property
    def validators(self):
        return [self.check_is_string]
