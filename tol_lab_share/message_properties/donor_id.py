from .message_property import MessageProperty


class DonorId(MessageProperty):
    @property
    def validators(self):
        return [self.check_is_string]
