from .Object import NetworkObject


class CarNumbers(NetworkObject):
    def __init__(self, numbers):
        super().__init__()
        self.numbers = numbers