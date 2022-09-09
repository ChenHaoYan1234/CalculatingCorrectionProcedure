# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import Values
import Tools


class Ui_SettingMenu(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        self.setupUi()

    def setupUi(self):
        self.setObjectName("SettingMenu")
        self.resize(300, 500)
        self.Setting = QtWidgets.QTabWidget(self)
        self.Setting.setGeometry(QtCore.QRect(0, 0, 300, 500))
        self.Setting.setObjectName("Setting")
        self.Custom = QtWidgets.QWidget()
        self.Custom.setObjectName("Custom")
        self.Background = QtWidgets.QLabel(self.Custom)
        self.Background.setGeometry(QtCore.QRect(0, 50, 300, 250))
        self.Background.setText("")
        self.Background.setObjectName("Background")
        self.Background.setScaledContents(True)
        self.bg = self.parent_window.bg
        self.Background.setPixmap(self.bg)
        self.SetBackground = QtWidgets.QPushButton(self.Custom)
        self.SetBackground.setGeometry(QtCore.QRect(100, 320, 100, 20))
        self.SetBackground.setObjectName("SetBackground")
        self.SetBackground.clicked.connect(self.setBackground)
        self.Setting.addTab(self.Custom, "")
        self.About = QtWidgets.QWidget()
        self.About.setObjectName("About")
        self.Author = QtWidgets.QLabel(self.About)
        self.Author.setGeometry(QtCore.QRect(0, 100, 300, 20))
        self.Author.setAlignment(QtCore.Qt.AlignCenter)
        self.Author.setObjectName("Author")
        self.Version = QtWidgets.QLabel(self.About)
        self.Version.setGeometry(QtCore.QRect(0, 120, 300, 20))
        self.Version.setAlignment(QtCore.Qt.AlignCenter)
        self.Version.setObjectName("Version")
        self.CheckUpdate = QtWidgets.QPushButton(self.About)
        self.CheckUpdate.setGeometry(QtCore.QRect(110, 180, 75, 30))
        self.CheckUpdate.setObjectName("CheckUpdate")
        self.CheckUpdate.clicked.connect(self.update)
        self.Setting.addTab(self.About, "")
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def setBackground(self):
        path = Tools.getPath(2, self)
        if not path:
            return 0
        self.bg = QtGui.QPixmap(path)
        self.Background.setPixmap(self.bg)

    def update(self):
        self.parent_window.bg = self.bg
        self.parent_window.Background.setPixmap(self.parent_window.bg)
        Tools.download_updater()
        Tools.found_upgrade(self)

    def closeEvent(self, event):
        self.parent_window.bg = self.bg
        self.parent_window.Background.setPixmap(self.parent_window.bg)
        event.accept()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("SettingMenu", "设置"))
        self.SetBackground.setText(_translate("SettingMenu", "选择背景图片"))
        self.Setting.setTabText(self.Setting.indexOf(
            self.Custom), _translate("SettingMenu", "个性化"))
        self.Author.setText(_translate("SettingMenu", "作者:"+Values.author))
        self.Version.setText(_translate("SettingMenu", "版本:"+Values.version))
        self.CheckUpdate.setText(_translate("SettingMenu", "检查更新"))
        self.Setting.setTabText(self.Setting.indexOf(
            self.About), _translate("SettingMenu", "关于"))
