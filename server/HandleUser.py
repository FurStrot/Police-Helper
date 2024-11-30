import socket
from API.NetworkObjects import *
from DataBase import write_to_db, read_db, Car
from User import User
import pickle


class HandleUser:
    def __init__(self, conn):
        self.conn: socket.socket = conn
        self.user = User(conn)
        self.receiver()

    def disconnect(self):
        self.conn.close()


    def receiver(self):
        while True:
            data = self.conn.recv(1024 * 16)
            if not data:
                self.disconnect()
                return

            self.handle_object(pickle.loads(data))

    def handle_object(self, object:NetworkObject):

        print(f"Received object:{object}")

        if isinstance(object, Auth):
            if object.password not in ["zzz1234Z1"]: # change list to somthing else (workaround)
                print("invalid password")
                self.disconnect()
                return
            self.user.SendObject(AuthAnswer())

        if isinstance(object, RequestCarNumbers):
            self.user.SendObject(CarNumbers([car.number for car in read_db()]))

        if isinstance(object, RegisterCar):
            write_to_db(Car(object.number, object.name, object.color, object.brand, object.model, object.still))

        if isinstance(object, RequestInfoByNumber):
            db = read_db()
            print(db)
            car: None | Car = None
            for _car in db:
                if _car.number == object.number:
                    car = _car
            if car:
                self.user.SendObject(InfoByNumberAnswer(
                    True,
                    car.number,
                    car.name,
                    car.color,
                    car.brand,
                    car.model,
                    car.stealed
                ))
            else:
                self.user.SendObject(InfoByNumberAnswer(False))

