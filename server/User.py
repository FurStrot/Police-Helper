import socket
from API.NetworkObjects import *


class User:
    def __init__(self, conn):
        self.conn:socket.socket = conn

    def SendObject(self, object:NetworkObject):
        self.conn.send(NetworkObject.serialize(object))