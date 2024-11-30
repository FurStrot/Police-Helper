from .Object import NetworkObject


class RequestInfoByNumber(NetworkObject):
    def __init__(self, number):
        super().__init__()
        self.number = number