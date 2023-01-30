from .message_property import MessageProperty


class Volume(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid volume provided by another
    MessageProperty.
    The volume has to be a float string.
    Eg: '43.335'
    """

    @property
    def validators(self):
        return [self.check_is_float_string]
