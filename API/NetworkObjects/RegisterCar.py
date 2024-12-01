from .Object import NetworkObject


class RegisterCar(NetworkObject):
    def __init__(self, number, name, color, brand, model, stolen):
        super().__init__()
        self.number = number
        self.name = name
        self.color = color
        self.brand = brand
        self.model = model
        self.stolen = stolen