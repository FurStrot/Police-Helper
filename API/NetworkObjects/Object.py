import pickle


class NetworkObject:
        def __init__(self):
            pass

        def serialize(self):
            return pickle.dumps(self)

        @staticmethod
        def deserialize(object):
            return pickle.loads(object)