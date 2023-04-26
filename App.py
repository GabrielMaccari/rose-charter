from PyQt6.QtWidgets import QApplication
from sys import argv

from View import MainWindow
from Controller import Controller

if __name__ == '__main__':
    try:
        app = QApplication(argv)

        with open('style/styles.qss', 'r') as f:
            style = f.read()
        app.setStyleSheet(style)

        controller = Controller()

        window = MainWindow(controller)
        window.show()
        app.exec()
    except Exception as exception:
        print(f"\n{exception.__class__}: {exception}")