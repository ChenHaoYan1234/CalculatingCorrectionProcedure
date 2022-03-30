import base64
import csv
import getpass
import os
import sys
import time
import requests
import ImageData
from PyQt5.QtWidgets import QMessageBox, QFileDialog


def getPath(mode: int, window) -> str:
    if mode == 0:
        path = QFileDialog.getOpenFileName(
            window,
            "请选择文件",
            os.path.dirname(os.path.realpath(sys.argv[0])),
            "Image File(*.jpg;*.jpge;*.png;*.bmp);;All File(*.*)"
        )
        if not os.path.isfile(path[0]):
            QMessageBox.critical(
                window,
                "错误",
                "请选择一张图片！",
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Ok
            )
            return False
        else:
            return path[0]
    elif mode == 1:
        path = QFileDialog.getExistingDirectory(
            window, "打开文件夹", os.path.dirname(os.path.realpath(sys.argv[0])))
        if not os.path.isdir(path):
            QMessageBox.critical(
                window,
                "错误",
                "请选择一个文件夹！",
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Ok
            )
            return False
        else:
            return path
    else:
        path = QFileDialog.getOpenFileName(
            window,
            "请选择文件",
            os.path.dirname(os.path.realpath(sys.argv[0])) +
            "\\bg\\",
            "Image File(*.jpg;*.jpge;*.png;*.bmp);;All File(*.*)"
        )
        if not os.path.isfile(path[0]):
            QMessageBox.critical(
                window,
                "错误",
                "请选择一张图片！",
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Ok
            )
            return False
        else:
            return path[0]


def getPhoto(path: str) -> bytes:
    file = open(path, 'rb')
    img = base64.b64encode(file.read())
    file.close()
    return img


def getPhotoFromPath(path: str, window) -> list:
    img_name_list = []
    img_base64_list = []
    if os.path.isdir(path):
        for file in os.listdir(path):
            if file.split(".")[-1] in ["jpg", "jpge", "png", "bmp"]:
                img_name_list.append(file)
                img_base64_list.append(getPhoto(path+"\\"+file))
        if len(img_name_list) == 0:
            QMessageBox.critical(window, "错误", "请选择一个有图片的文件夹！",
                                 QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return False
        else:
            return [img_name_list, img_base64_list]
    else:
        QMessageBox.critical(window, "错误", "请选择一个文件夹！",
                             QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
        return [False, False]


def getAccessToken(client_id: str, client_secret: str, window) -> str:
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + \
        client_id+'&client_secret='+client_secret
    try:
        response = requests.get(host)
    except:
        msg = QMessageBox.critical(
            window,
            "错误",
            "请求失败!请检查是否连接因特网后重试。",
            QMessageBox.StandardButton.Retry |
            QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Retry
        )
        if msg == QMessageBox.StandardButton.Retry:
            return getAccessToken(client_id, client_secret, window)
        else:
            return False
    if response and (not ("error_msg" in response.json())):
        access_token = response.json()["access_token"]
        return access_token
    else:
        msg = QMessageBox.critical(
            window,
            "错误",
            "请求失败!服务异常,请稍后重试。",
            QMessageBox.StandardButton.Retry |
            QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Retry
        )
        if msg == QMessageBox.StandardButton.Retry:
            return getAccessToken(client_id, client_secret, window)
        else:
            return False


def hasProp(obj: dict, prop: str):
    try:
        temp = obj[prop]
        del temp
        return True
    except Exception:
        return False


def getDistinguishResult(base64_photo: bytes, access_token: str, window, db: ImageData.ImageData) -> dict:
    if db.getResultFromImage(base64_photo) != None:
        return db.getResultFromImage(base64_photo)
    host = "https://aip.baidubce.com/rest/2.0/ocr/v1/doc_analysis"
    params = {"image": base64_photo,
              "language_type": "CHN_ENG", "result_type": "big"}
    host = host + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    try:
        response = requests.post(host, data=params, headers=headers)
    except:
        msg = QMessageBox.critical(
            window,
            "错误",
            "请求失败!请检查是否连接因特网后重试。",
            QMessageBox.StandardButton.Retry |
            QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Retry
        )
        if msg == QMessageBox.StandardButton.Retry:
            return getDistinguishResult(base64_photo, access_token, window, db)
        else:
            return False
    if response and (not ("error_msg" in response.json())):
        result = response.json()
        db.newResult(base64_photo, result)
        return result
    else:
        msg = QMessageBox.critical(
            window,
            "错误",
            "请求失败!服务异常,请稍后重试。",
            QMessageBox.StandardButton.Retry |
            QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Retry
        )
        print(response.json())
        if msg == QMessageBox.StandardButton.Retry:
            return getDistinguishResult(base64_photo, access_token, window, db)
        else:
            return False


def resultParser(result: dict, window) -> list:
    try:
        result_len = len(result["results"])
        result_list = []
        for i in range(result_len):
            temp_text: str = result["results"][i]["words"]["word"]
            temp_text = temp_text.split("=")
            if len(temp_text) != 2:
                QMessageBox.critical(
                    window,
                    "错误",
                    "请确定图片内只有题目!",
                    QMessageBox.StandardButton.Ok,
                    QMessageBox.StandardButton.Ok
                )
                return False
            temp_print: str = temp_text[0]
            temp_handwriting: str = temp_text[1]
            temp_handwriting = float(eval(temp_handwriting.replace("/", "1")))
            temp_1 = temp_print
            temp_1 = temp_1.replace("×", "*")
            temp_1 = temp_1.replace("x", "*")
            temp_1 = temp_1.replace("÷", "/")
            temp_answer = float(eval(temp_1))
            temp_right = "✓" if (float(temp_handwriting)
                                 == temp_answer) else "✗"
            temp_print = temp_print.replace("*", "×")
            temp_print = temp_print.replace("/", "÷")
            temp_result = [temp_print, temp_handwriting,
                           temp_answer, temp_right]
            result_list.append(temp_result)
        return result_list
    except:
        QMessageBox.critical(
            window,
            "错误",
            "书写不规范！",
            QMessageBox.StandardButton.Ok,
            QMessageBox.StandardButton.Ok
        )
        return False


def resultsParser(results: list, window=None) -> list:
    results_ = []
    for i in results:

        results_.append(resultParser(i, window))
        if False in results_:
            return [False, ]
    return results_


def getMode(window) -> 0 | 1:
    msg = QMessageBox(QMessageBox.Icon.Question, "请选择口算图片打开方式", "请选择口算图片打开方式")
    file_btn = msg.addButton(window.tr("打开文件"), QMessageBox.ButtonRole.YesRole)
    dir_btn = msg.addButton(window.tr("打开文件夹"), QMessageBox.ButtonRole.NoRole)
    msg.setDefaultButton(file_btn)
    msg.setEscapeButton(file_btn)
    msg.exec_()
    if msg.clickedButton() == file_btn:
        return 0
    else:
        return 1


def saveResult(result: list, mode: int, window, file_or_dir_name=None) -> None:
    if mode == 0:
        path = QFileDialog.getSaveFileName(
            window,
            "请选择保存路径",
            os.path.dirname(os.path.realpath(sys.argv[0])) +
            "\\" +
            file_or_dir_name.split(".")[0] +
            "-" +
            time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) +
            ".csv",
            "CSV File(*.csv);;All File(*.*)"
        )
        path = path[0]
    elif mode == 1:
        path: str = QFileDialog.getExistingDirectory(
            window,
            "请选择保存文件夹",
            os.path.dirname(os.path.realpath(sys.argv[0]))
        )
    else:
        raise ValueError("Unknow Mode!")
    if path.replace(" ", "") == "":
        QMessageBox.critical(window,
                             "错误",
                             "请确认你选择了一个正确的路径!",
                             QMessageBox.StandardButton.Ok,
                             QMessageBox.StandardButton.Ok
                             )
        return 0
    if mode == 0:
        try:
            result_file = open(path, "w", encoding="utf-8")
            writer = csv.writer(result_file)
            writer.writerow(["题目", "学生答案", "正确答案", "对错"])
            for one in result:
                writer.writerow(one)
            result_file.close()
            QMessageBox.information(
                window,
                "保存成功",
                "已保存至" +
                path,
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Ok
            )
        except PermissionError:
            QMessageBox.critical(
                window,
                "错误",
                "权限不足！",
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Ok
            )
            return 0
        except Exception as e:
            QMessageBox.critical(
                window,
                "错误",
                "未知错误！\n错误信息"+str(e.args),
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Ok
            )
            return 0
    else:
        for i in range(0, len(result)):
            try:
                name: str = file_or_dir_name[i]
                name = name.replace("jpge", "csv")
                name = name.replace("jpg", "csv")
                name = name.replace("bmp", "csv")
                name = name.replace("png", "csv")
                result_file = open(path+"\\"+name, "w", encoding="utf-8")
                writer = csv.writer(result_file)
                writer.writerow(["题目", "学生答案", "正确答案", "对错"])
                for one in result[i]:
                    writer.writerow(one)
                result_file.close()

            except PermissionError:
                QMessageBox.critical(
                    window,
                    "错误",
                    "权限不足！",
                    QMessageBox.StandardButton.Ok,
                    QMessageBox.StandardButton.Ok
                )
            except Exception as e:
                QMessageBox.critical(
                    window,
                    "错误",
                    "未知错误！\n错误信息"+str(e.args),
                    QMessageBox.StandardButton.Ok,
                    QMessageBox.StandardButton.Ok
                )
        QMessageBox.information(
            window,
            "保存成功",
            "已保存至" +
            path,
            QMessageBox.StandardButton.Ok,
            QMessageBox.StandardButton.Ok
        )
