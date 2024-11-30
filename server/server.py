import socket
import HandleUser
import config

sock = socket.socket()
sock.bind((config.server_adress, config.server_port))
sock.listen(5)

print("Server is listening")

while True:
    conn, addr = sock.accept()
    print("connection from", addr)
    HandleUser.HandleUser(conn)
