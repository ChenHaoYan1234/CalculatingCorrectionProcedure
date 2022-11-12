# -*- coding: utf-8 -*-
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

import ImageData
import SettingMenu
import Tools
import Values


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(600, 500)
        self.setFixedSize(self.width(), self.height())
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.Main = QtWidgets.QFrame(self.centralwidget)
        self.Main.setGeometry(QtCore.QRect(0, 0, 600, 500))
        self.Main.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.Main.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.Main.setObjectName("Main")
        self.bg = QtGui.QPixmap(os.path.dirname(
            os.path.realpath(sys.argv[0]))+"\\bg\\bg2.png")
        self.Background = QtWidgets.QLabel(self.Main)
        self.Background.setGeometry(QtCore.QRect(0, 0, 600, 500))
        self.Background.setText("")
        self.Background.setPixmap(self.bg)
        self.Background.setScaledContents(True)
        self.Background.setObjectName("Background")
        self.Title = QtWidgets.QLabel(self.Main)
        self.Title.setGeometry(QtCore.QRect(160, 60, 280, 60))
        font = QtGui.QFont()
        font.setPointSize(34)
        self.Title.setFont(font)
        self.Title.setObjectName("Title")
        self.OpenImage = QtWidgets.QPushButton(self.Main)
        self.OpenImage.setGeometry(QtCore.QRect(150, 350, 100, 40))
        self.OpenImage.setObjectName("OpenImage")
        self.OpenImage.clicked.connect(self.openPhotoEvent)
        self.Setting = QtWidgets.QPushButton(self.Main)
        self.Setting.setGeometry(QtCore.QRect(250, 350, 100, 40))
        self.Setting.setObjectName("Setting")
        self.Setting.clicked.connect(self.setting)
        self.Exit = QtWidgets.QPushButton(self.Main)
        self.Exit.setGeometry(QtCore.QRect(350, 350, 100, 40))
        self.Exit.setObjectName("Exit")
        self.Exit.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.Help = QtWidgets.QLabel(self.Main)
        self.Help.setGeometry(QtCore.QRect(100, 120, 400, 200))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Help.setFont(font)
        self.Help.setObjectName("label")
        self.Wait = QtWidgets.QFrame(self.centralwidget)
        self.Wait.setGeometry(QtCore.QRect(0, 0, 600, 500))
        self.Wait.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.Wait.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.Wait.setObjectName("Wait")
        self.WaitText = QtWidgets.QLabel(self.Wait)
        self.WaitText.setGeometry(QtCore.QRect(300, 200, 290, 100))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.WaitText.setFont(font)
        self.WaitText.setObjectName("WaitText")
        self.WaitIcon = QtWidgets.QLabel(self.Wait)
        self.WaitIcon.setGeometry(QtCore.QRect(100, 150, 200, 200))
        self.WaitIcon.setText("")
        self.WaitGif = QtGui.QMovie(".\\resource\\loading.git")
        self.WaitIcon.setMovie(self.WaitGif)
        self.WaitGif.start()
        self.WaitIcon.setObjectName("WaitIcon")
        self.setCentralWidget(self.centralwidget)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.showMain()
        self.db = ImageData.ImageData(
            os.path.dirname(os.path.realpath(sys.argv[0]))+"\\image.db")
        try:
            sys.argv[1]
            QtWidgets.QMessageBox.information(self, "", "已更新至"+Values.version+"。",
                                              QtWidgets.QMessageBox.StandardButton.Ok, QtWidgets.QMessageBox.StandardButton.Ok)
        except:
            pass

    def closeEvent(self, event):
        self.db.close()
        event.accept()

    def showMain(self):
        self.Main.setVisible(True)
        self.Wait.setVisible(False)

    def showWait(self):
        self.Main.setVisible(False)
        self.Wait.setVisible(True)

    def openPhotoEvent(self):
        self.showWait()
        mode = Tools.getMode(self)
        if mode == 2:
            return 0
        path = Tools.getPath(mode, self)
        access_token = Tools.getAccessToken(
            Values.client_id, Values.client_secret, self)
        if access_token == False:
            self.showMain()
            return 0
        if not path:
            self.showMain()
            return 0
        if mode == 0:
            temp = Tools.getPhoto(path)
            if temp:
                base64_photo = temp
            else:
                self.showMain()
                return 0
            result = Tools.getDistinguishResult(
                base64_photo, access_token, self, self.db)
            if result == False:
                self.showMain()
                return 0
            result = Tools.resultParser(result, self)
            if result == False:
                self.showMain()
                return 0
            Tools.saveResult(result, mode, self, path)
            self.showMain()
        else:
            img_ = Tools.getPhotoFromPath(path, self)
            if img_ == False:
                self.showMain()
                return 0
            path_list: list[str] = img_[0]
            img_list: list[bytes] = img_[1]
            results = []
            for i in img_list:
                results.append(Tools.getDistinguishResult(
                    i, access_token, self, self.db))
            results = Tools.resultsParser(results, self)
            if results == False:
                self.showMain()
                return 0
            Tools.saveResult(results, mode, self)
            self.showMain()

    def setting(self):
        setting = SettingMenu.Ui_SettingMenu(self)
        setting.show()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "口算批改程序"))
        self.Title.setText(_translate("MainWindow", "口算批改程序"))
        self.OpenImage.setText(_translate("MainWindow", "打开图片"))
        self.Setting.setText(_translate("MainWindow", "设置"))
        self.Exit.setText(_translate("MainWindow", "退出"))
        self.Help.setText(_translate("MainWindow", "请点击开始识别按钮以开始识别。"))
        self.WaitText.setText(_translate("MainWindow", "正在识别中,请等一下。"))
