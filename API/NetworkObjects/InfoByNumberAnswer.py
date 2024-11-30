from .Object import NetworkObject


class InfoByNumberAnswer(NetworkObject):
    def __init__(self, found, number=None, name=None, color=None, brand=None, model=None, stealed=None):
        super().__init__()
        self.number = number
        self.name = name
        self.color = color
        self.brand = brand
        self.model = model
        self.stealed = stealed
        self.found = found

