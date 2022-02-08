import os
import sys
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *

SCREEN_SIZE = [600, 450]
coords = "37.404304, 55.652923"
spn = '1'


class Example(QWidget):
    def __init__(self, coords, spn):
        super().__init__()
        self.coords = coords.replace(' ', '')
        self.spn_input = spn
        self.spn = self.spn_input + ',' + '' + self.spn_input
        self.coords_x, self.coords_y = self.coords.split(',')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.getImage()

    def keyPressEvent(self, event):
        self.coords_x, self.coords_y = self.coords.split(',')
        if event.key() == Qt.Key_PageDown:
            if float(self.spn_input) < 40:
                self.spn_input = str(float(self.spn_input) + 0.6)[:5]
        if event.key() == Qt.Key_PageUp:
            if float(self.spn_input) > 0.41:
                self.spn_input = str(float(self.spn_input) - 0.4)[:5]
            if float(self.spn_input) > 0.11 and float(self.spn_input) < 0.4:
                self.spn_input = str(float(self.spn_input) - 0.1)[:5]
            if float(self.spn_input) > 0.021 and float(self.spn_input) < 0.1:
                self.spn_input = str(float(self.spn_input) - 0.02)[:5]
            if float(self.spn_input) > 0.0021 and float(self.spn_input) < 0.02:
                self.spn_input = str(float(self.spn_input) - 0.002)[:5]
        if event.key() == Qt.Key_Up:
            if float(self.coords_y) < 84:
                if float(self.spn_input) > 1:
                    self.coords_y = float(float(self.coords_y) + 0.5)
                if float(self.spn_input) > 0.3 and float(self.spn_input) <= 1:
                    self.coords_y = float(float(self.coords_y) + 0.05)
                if float(self.spn_input) > 0.05 and float(self.spn_input) <= 0.3:
                    self.coords_y = float(float(self.coords_y) + 0.03)
                if float(self.spn_input) > 0.001 and float(self.spn_input) <= 0.05:
                    self.coords_y = float(float(self.coords_y) + 0.001)
        if event.key() == Qt.Key_Down:
            if float(self.coords_y) > -84:
                if float(self.spn_input) > 1:
                    self.coords_y = float(float(self.coords_y) - 0.5)
                if float(self.spn_input) > 0.3 and float(self.spn_input) <= 1:
                    self.coords_y = float(float(self.coords_y) - 0.05)
                if float(self.spn_input) > 0.05 and float(self.spn_input) <= 0.3:
                    self.coords_y = float(float(self.coords_y) - 0.03)
                if float(self.spn_input) > 0.001 and float(self.spn_input) <= 0.05:
                    self.coords_y = float(float(self.coords_y) - 0.001)
        if event.key() == Qt.Key_Right:
            if float(self.coords_x) < 179.99:
                if float(self.spn_input) > 1:
                    self.coords_x = float(float(self.coords_x) + 0.5)
                if float(self.spn_input) > 0.3 and float(self.spn_input) <= 1:
                    self.coords_x = float(float(self.coords_x) + 0.05)
                if float(self.spn_input) > 0.05 and float(self.spn_input) <= 0.3:
                    self.coords_x = float(float(self.coords_x) + 0.03)
                if float(self.spn_input) > 0.001 and float(self.spn_input) <= 0.05:
                    self.coords_x = float(float(self.coords_x) + 0.001)
        if event.key() == QtCore.Qt.Key_Left:
            if float(self.coords_x) > -179.99:
                if float(self.spn_input) > 1:
                    self.coords_x = float(float(self.coords_x) - 0.5)
                if float(self.spn_input) > 0.3 and float(self.spn_input) <= 1:
                    self.coords_x = float(float(self.coords_x) - 0.05)
                if float(self.spn_input) > 0.05 and float(self.spn_input) <= 0.3:
                    self.coords_x = float(float(self.coords_x) - 0.03)
                if float(self.spn_input) > 0.001 and float(self.spn_input) <= 0.05:
                    self.coords_x = float(float(self.coords_x) - 0.001)
        self.getImage()

    def getImage(self):
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        self.spn = self.spn_input + ',' + '' + self.spn_input
        self.coords = str(self.coords_x) + ',' + str(self.coords_y)

        map_params = {
            "ll": self.coords,
            "spn": self.spn,
            "l": "map"}
        self.response = requests.get(map_api_server, params=map_params)

        if not self.response:
            print("Ошибка выполнения запроса:")
            print(self.response.url)
            print("Http статус:", self.response.status_code, "(", self.response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(self.response.content)

        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example(coords, spn)
    ex.show()
    sys.exit(app.exec())
