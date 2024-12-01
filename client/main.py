import pickle
import sys
import os
import json
import webbrowser
import subprocess
import socket
import threading
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt6.QtGui import QFont
from time import sleep
import config
from API.NetworkObjects import *

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.side_1 = uic.loadUi('police_helper.ui', self)

        self.connect()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ("127.0.0.1", 9090)
        self.connect_to_server()
        self.send_object(Auth(config.password))
        if self.receive_and_handle():
            print("Authenticated")
        else:
            QMessageBox.critical(self, "Authentication Error", f"Password may be incorrect")

        self.number_cars = []

        self.car_numbder.hide()
        self.ticket.hide()
        self.registration.hide()

        threading.Thread(target=self.numbers_update_cycle).start()

    def numbers_update_cycle(self):
        while True:
            self.send_object(RequestCarNumbers())
            self.receive_and_handle()
            sleep(20)

    def connect(self):
        self.btn_tikcet.clicked.connect(self.show_ticket)
        self.btn_car_number.clicked.connect(self.show_car_numbers)
        self.btn_regisn_number.clicked.connect(self.show_registration)
        self.btn_furstrot.clicked.connect(self.open_webbrowser)
        self.btn_create.clicked.connect(self.create_ticket)

        self.btn_find.clicked.connect(self.found_number)

        self.crn_btn_create.clicked.connect(self.add_number)

        self.btn_exit.clicked.connect(self.exit)
        self.cn_btn_exit.clicked.connect(self.back_menu)
        self.t_btn_exit.clicked.connect(self.back_menu)
        self.crn_btn_exit.clicked.connect(self.back_menu)

    def show_ticket(self):
        self.ticket.show()
        self.btn_regisn_number.hide()

    def show_car_numbers(self):
        self.car_numbder.show()
        self.btn_regisn_number.hide()

    def show_registration(self):
        self.btn_regisn_number.hide()
        self.registration.show()

    def open_webbrowser(self):
        url = "https://github.com/FurStrot"
        webbrowser.open(url)

    def back_menu(self):
        self.ticket.hide()
        self.car_numbder.hide()
        self.registration.hide()
        self.btn_regisn_number.show()

    def exit(self):
        self.socket.close()
        sys.exit()

    def connect_to_server(self):
        try:
            self.socket.connect(self.server_address)
            print("Connected to server")
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", f"Error connecting to server: {e}")
            sys.exit()

    def send_object(self, obj):
        serialized_object = NetworkObject.serialize(obj)
        self.socket.send(serialized_object)

    def create_ticket(self):
        ticket_info = { #may be can change it to class
            "badge_number": self.t_line_badge.text(),
            "name_officer": self.t_line_name_officer.text(),
            "name_pepole": self.t_line_name.text(),
            "order": self.t_line_order.text(),
            "sum_order": self.sum_order.value(),
        }

        with open("ticket_give.txt", "w") as file:
            file.write(
                f"Name officer: {ticket_info['name_officer']}, badge number: {ticket_info['badge_number']}\n"
                f"\nName citizen: {ticket_info['name_pepole']}\n\n"
                f"Sum order: ${ticket_info['sum_order']}\n\n")

        subprocess.run(["notepad", "ticket_give.txt"])

    def add_number(self):
        number = self.line_number.text()
        name = self.line_name.text()
        color = self.line_color.text()
        brand = self.line_breand.text()
        model = self.line_model.text()
        status = self.line_still.text()

        fields = {
            "Number": number,
            "Name": name,
            "Color": color,
            "Brand": brand,
            "Model": model,
            "Still": status
        }

        missing_fields = [field_name for field_name, value in fields.items() if not value]

        if missing_fields:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Please fill in the following fields:")
            msg.setWindowTitle("ERROR")
            msg.setDetailedText("\n".join(missing_fields))
            msg.exec()
            return

        register_car_obj = RegisterCar(number, name, color, brand, model, status)
        self.send_object(register_car_obj)

        QMessageBox.information(self, "Success", "Car registered successfully.")

    def found_number(self):
        font = QFont("Impact", 8, QFont.Weight.Bold, italic=True)
        font.setPointSize(20)

        self.cn_info_number.setFont(font)
        self.cn_info_name.setFont(font)
        self.cn_info_color.setFont(font)
        self.cn_info_breand.setFont(font)
        self.cn_info_model.setFont(font)
        self.cn_info_still.setFont(font)

        car_number = self.line_car_number.text()
        self.send_object(RequestInfoByNumber(car_number))
        response = self.receive_and_handle()

        if response.found:
            self.cn_info_number.setText(response.number)
            self.cn_info_name.setText(response.name)
            self.cn_info_color.setText(response.color)
            self.cn_info_breand.setText(response.brand)
            self.cn_info_model.setText(response.model)
            self.cn_info_still.setText(response.stolen) #stealed
        else:
            self.show_error_message("Car not found.")

    def show_error_message(self, message):
        self.cn_info_number.setText("ERROR")
        self.cn_info_name.setText("ERROR")
        self.cn_info_color.setText("ERROR")
        self.cn_info_breand.setText("ERROR")
        self.cn_info_model.setText("ERROR")
        self.cn_info_still.setText("ERROR")
        QMessageBox.warning(self, "Error", message)

    def receive_and_handle(self):
        while True:
            data = self.socket.recv(1024 * 16)
            if not data:
                return False

            return self.handle_object(pickle.loads(data))

    def handle_object(self, object:NetworkObject):
        if isinstance(object, AuthAnswer):
            return True

        if isinstance(object, CarNumbers):
            self.number_cars = object.numbers # can replace extend to =
            return True

        if isinstance(object, InfoByNumberAnswer):
            return object

        return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    app.setStyle('windows11')
    ex.show()
    sys.exit(app.exec())

#TODO: Нужно сделать получение номеров маашин и получение информации по номеру