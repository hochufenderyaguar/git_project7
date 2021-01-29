import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QStyleFactory, QMainWindow, QTableWidgetItem


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.select_data()

    def select_data(self):
        res = self.connection.cursor().execute(f'''SELECT * FROM data''').fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки'])
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

        self.tableWidget.resizeColumnsToContents()

    def closeEvent(self, event):
        self.connection.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))

    win = Window()
    win.show()

    sys.excepthook = except_hook
    sys.exit(app.exec())
