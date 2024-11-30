import socket
import json
import config

sock = socket.socket()
sock.connect((config.server_adress, config.server_port))


