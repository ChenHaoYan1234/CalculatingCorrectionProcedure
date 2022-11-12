# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QApplication

import MainWindow


def main():
    Application = QApplication(sys.argv)
    Window = MainWindow.Ui_MainWindow()
    Window.show()
    sys.exit(Application.exec_())


if __name__ == "__main__":
    main()
