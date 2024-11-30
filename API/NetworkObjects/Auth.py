from .Object import NetworkObject


class Auth(NetworkObject):
    def __init__(self, password):
        super().__init__()
        self.password = password
        