# -*- coding: utf-8 -*-
import sys

from PySide6.QtWidgets import QApplication

import ui.MainWindow


def main():
    Application = QApplication(sys.argv)
    Window = ui.MainWindow.Ui_MainWindow()
    Window.show()
    sys.exit(Application.exec())


if __name__ == "__main__":
    main()
