import sys
import os
import json
import webbrowser
import subprocess

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt6.QtGui import QFont


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.side_1 = uic.loadUi('police_helper.ui', self)
        self.connect()

        self.ticket_information = []
        self.number_cars = []

        self.car_numbder.hide()
        self.ticket.hide()
        self.registration.hide()

        if os.path.exists("car_infos.json"):
            with open("car_infos.json", "r") as file:
                self.number_cars = json.load(file)

        if os.path.exists("ticket.json"):
            with open("ticket.json", "r") as file:
                self.ticket_information = json.load(file)

    def connect(self):
        #menu
        self.btn_tikcet.clicked.connect(self.show_ticket)
        self.btn_car_number.clicked.connect(self.show_car_numbers)
        self.btn_regisn_number.clicked.connect(self.show_registration)
        self.btn_furstrot.clicked.connect(self.open_webbrowser)
        self.btn_create.clicked.connect(self.create_ticket)

        #show_car_numbder
        self.btn_find.clicked.connect(self.found_number)

        #create_car_number
        self.crn_btn_create.clicked.connect(self.add_number)

        #exits
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
        sys.exit()

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

        for index, car in enumerate(self.number_cars):
            if car["number"] == number:
                self.number_cars[index] = {
                    "number": number,
                    "name": name,
                    "color": color,
                    "brand": brand,
                    "model": model,
                    "status": status
                }
                break
        else:
            car_info = {
                "number": number,
                "name": name,
                "color": color,
                "brand": brand,
                "model": model,
                "status": status
            }
            self.number_cars.append(car_info)

        with open("car_infos.json", "w") as file:
            json.dump(self.number_cars, file)

    def found_number(self):
        font = QFont("Impact", 8, QFont.Weight.Bold, italic=True)
        font.setPointSize(20)

        self.cn_info_number.setFont(font)
        self.cn_info_name.setFont(font)
        self.cn_info_color.setFont(font)
        self.cn_info_breand.setFont(font)
        self.cn_info_model.setFont(font)
        self.cn_info_still.setFont(font)
        try:
            found = False
            car_number = self.line_car_number.text()
            for car in self.number_cars:
                if car["number"] == car_number:
                    self.cn_info_number.setText(car["number"])
                    self.cn_info_name.setText(car["name"])
                    self.cn_info_color.setText(car["color"])
                    self.cn_info_breand.setText(car["brand"])
                    self.cn_info_model.setText(car["model"])
                    self.cn_info_still.setText(car["status"])
                    found = True
                    break

            if not found:
                self.cn_info_number.setText("ERROR")
                self.cn_info_name.setText("ERROR")
                self.cn_info_color.setText("ERROR")
                self.cn_info_breand.setText("ERROR")
                self.cn_info_model.setText("ERROR")
                self.cn_info_still.setText("ERROR")

        except Exception as ex:
            print(ex)

    def create_ticket(self):
        ticket_info = {
            "badge_number": self.t_line_badge.text(),
            "name_officer": self.t_line_name_officer.text(),
            "name_pepole": self.t_line_name.text(),
            "order": self.t_line_order.text(),
            "sum_order": self.sum_order.value(),
        }

        self.ticket_information.append(ticket_info)

        with open("ticket.json", "w") as file:
            json.dump(self.ticket_information, file)

        with open("ticket_give.txt", "w") as file:
            file.write(
                f"Name officer: {ticket_info["name_officer"]}, badge number: {ticket_info["badge_number"]}"
                f"\n\nName citizen: {ticket_info["name_pepole"]}\n\n"
                f"Sum order: ${ticket_info["sum_order"]}\n\n")

        subprocess.run(["notepad", "ticket_give.txt"])


if __name__ == "__main__":
     app = QApplication(sys.argv)
     ex = App()
     app.setStyle('windows11')
     ex.show()
     sys.exit(app.exec())