import os
import sys
import py7zr
import requests
import win32api
import win32con
import Values


def download_upgrade():
    upgarde = requests.get(Values.upgrade_url+"latest/", allow_redirects=True)
    temp = open(os.getenv("TEMP")+"\\upgrade.7z", "wb")
    temp.write(upgarde.content)
    temp.close()


def extra_file():
    upgrade = py7zr.SevenZipFile(os.getenv("TEMP")+"\\upgrade.7z", "r")
    upgrade.extractall(os.path.dirname(os.path.realpath(sys.argv[0]))+"\\")
    upgrade.close()
    os.remove(os.getenv("TEMP")+"\\upgrade.7z")


def main():
    try:
        download_upgrade()
        extra_file()
        win32api.MessageBox(0, "更新成功!", "", win32con.MB_OK)
        os.execv(os.path.dirname(os.path.realpath(
            sys.argv[0]))+"\\Main.exe", ("first_run"))
    except:
        win32api.MessageBox(0, "更新失败！", "错误", win32con.MB_OK)
        sys.exit(0)


if __name__ == "__main__":
    main()
