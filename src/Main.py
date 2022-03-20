import sys
import MainWindow
from PyQt5.QtWidgets import QApplication


class UI_MainWindow(MainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(UI_MainWindow, self).__init__(parent=parent)
        self.setupUi(self)


def main():
    Application = QApplication(sys.argv)
    MainUI = UI_MainWindow()
    MainUI.show()
    sys.exit(Application.exec_())


if __name__ == "__main__":
    main()
