import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from mainwindow import ToDoApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("images/icon.png"))  # Установка иконки приложения
    window = ToDoApp()
    window.show()
    sys.exit(app.exec())