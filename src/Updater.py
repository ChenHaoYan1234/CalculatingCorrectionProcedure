# -*- coding: utf-8 -*-
import os
import sys

import py7zr
import requests
from PySide6.QtWidgets import QMessageBox

import Values

if sys.platform == "win32":
    temp_dir = os.getenv("TEMP", "C:/Windows/Temp")
elif sys.platform == "linux":
    temp_dir = os.getenv("TEMP", "/tmp")
else:
    temp_dir = os.getenv("TEMP", "/tmp")


def download_update():
    update = requests.get(Values.update_url+"latest/", allow_redirects=True)
    temp = open(temp_dir+"/update.7z", "wb")
    temp.write(update.content)
    temp.close()


def extra_file():
    update = py7zr.SevenZipFile(
        temp_dir+"/update.7z", "r")
    update.extractall(os.path.dirname(os.path.realpath(sys.argv[0]))+"/")
    update.close()
    os.remove(temp_dir+"/update.7z")


def main():
    try:
        download_update()
        extra_file()
        QMessageBox.information(
            None,  # type: ignore
            "",
            "更新成功！",
            QMessageBox.StandardButton.Ok,
            QMessageBox.StandardButton.Ok
        )
        os.execv(os.path.dirname(os.path.realpath(
            sys.argv[0]))+"/Main.exe", ("first_run",))
    except:
        QMessageBox.information(
            None,  # type: ignore
            "错误",
            "更新失败!",
            QMessageBox.StandardButton.Ok,
            QMessageBox.StandardButton.Ok
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
