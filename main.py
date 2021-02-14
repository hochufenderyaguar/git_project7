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
        self.pushButton.clicked.connect(self.add_click)
        self.pushButton_2.clicked.connect(self.red_click)
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

    def add_click(self):
        self.win1 = Add()
        self.win1.show()

    def red_click(self):
        try:
            self.win2 = Red(self.tableWidget.selectedItems()[0].row())
            self.win2.show()
        except Exception:
            pass


class Add(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Добавление')
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.click)

    def click(self):
        self.con = sqlite3.connect("coffee.sqlite")
        cur = self.con.cursor()
        try:
            cur.execute(f'''INSERT INTO data VALUES ({self.lineEdit_2.text()}, '{self.lineEdit_6.text()}', 
            '{self.lineEdit.text()}', '{self.lineEdit_5.text()}', '{self.lineEdit_3.text()}', 
{self.lineEdit_4.text()}, {self.lineEdit_7.text()}) ''')
            self.con.commit()
        except Exception:
            pass
        self.con.close()
        win.select_data()
        self.close()


class Red(QMainWindow):
    def __init__(self, row):
        super().__init__()
        self.row = row
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Редактирование')
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.click)
        self.con = sqlite3.connect("coffee.sqlite")
        self.res = self.con.cursor().execute(f'''SELECT * FROM data''').fetchall()[self.row]

        self.lineEdit_2.setText(str(self.res[0]))
        self.lineEdit_6.setText(str(self.res[1]))
        self.lineEdit.setText(str(self.res[2]))
        self.lineEdit_5.setText(str(self.res[3]))
        self.lineEdit_3.setText(str(self.res[4]))
        self.lineEdit_4.setText(str(self.res[5]))
        self.lineEdit_7.setText(str(self.res[6]))

    def click(self):
        cur = self.con.cursor()
        try:
            cur.execute(
                f'''UPDATE data SET ID='{self.lineEdit_2.text()}', "название сорта"='{self.lineEdit_6.text()}', 
                           "степень обжарки"='{self.lineEdit.text()}', "молотый/в зернах"='{self.lineEdit_5.text()}', 
                           "описание вкуса"='{self.lineEdit_3.text()}', цена={self.lineEdit_4.text()}, 
                           "объем упаковки"={self.lineEdit_7.text()} WHERE ID = {self.res[0]}''')
            self.con.commit()
        except Exception:
            pass
        self.con.close()
        win.select_data()
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))

    win = Window()
    win.show()

    sys.excepthook = except_hook
    sys.exit(app.exec())
