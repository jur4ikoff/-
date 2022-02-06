import os
import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from check_coord import check_spn as chk_spn

SCREEN_SIZE = [600, 450]
coords = input('Введите координаты через запятую: ')  # coord1, coord2
spn = input('Введите масштаб: ')


class Example(QWidget):
    def __init__(self, coords, spn):
        super().__init__()
        self.coords = coords.replace(' ', '')
        self.spn = spn
        self.spn = self.spn + ',' + '' + self.spn
        self.getImage()
        self.initUI()

    def getImage(self):
        map_api_server = "http://static-maps.yandex.ru/1.x/"
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

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example(coords, spn)
    ex.show()
    sys.exit(app.exec())
