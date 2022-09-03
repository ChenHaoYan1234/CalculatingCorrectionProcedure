# -*- coding: utf-8 -*-
import sys
import MainWindow
import Values
from PyQt5.QtWidgets import QApplication


def main():
    try:
        if sys.argv[1] == "first_run":
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox(None, "", "已更新至"+Values.version+"。",
                        QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
    except:
        pass
    Application = QApplication(sys.argv)
    Window = MainWindow.Ui_MainWindow()
    Window.show()
    sys.exit(Application.exec_())


if __name__ == "__main__":
    main()
