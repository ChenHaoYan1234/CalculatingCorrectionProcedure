import os
import sys
import py7zr
import requests
import win32api
import win32con
import Values


def download_update():
    update = requests.get(Values.update_url+"latest/", allow_redirects=True)
    temp = open(os.getenv("TEMP")+"\\update.7z", "wb")
    temp.write(update.content)
    temp.close()


def extra_file():
    update = py7zr.SevenZipFile(os.getenv("TEMP")+"\\update.7z", "r")
    update.extractall(os.path.dirname(os.path.realpath(sys.argv[0]))+"\\")
    update.close()
    os.remove(os.getenv("TEMP")+"\\update.7z")


def main():
    try:
        download_update()
        extra_file()
        win32api.MessageBox(0, "更新成功!", "", win32con.MB_OK)
        os.execv(os.path.dirname(os.path.realpath(
            sys.argv[0]))+"\\Main.exe", ("first_run",))
    except:
        win32api.MessageBox(0, "更新失败！", "错误", win32con.MB_OK)
        sys.exit(0)


if __name__ == "__main__":
    main()
