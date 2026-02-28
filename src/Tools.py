# -*- coding: utf-8 -*-
import base64
import csv
import os
import sys
import time
from typing import Any, Literal, Optional

import requests
from PySide6.QtWidgets import QFileDialog, QMessageBox, QWidget

import Values
from ImageData import ImageData
from Values import STATUS


def getPath(mode: int, window:QWidget) -> str | Literal[STATUS.ERROR]:
    if mode == 0:
        path = QFileDialog.getOpenFileName(
            window,
            "请选择文件",
            os.path.dirname(os.path.realpath(sys.argv[0])),
            "Image File(*.jpg;*.jpge;*.png;*.bmp);;All File(*.*)"
        )[0]
        if not os.path.isfile(path):
            QMessageBox.critical(
                window,
                "错误",
                "请选择一张图片！",
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Ok
            )
            return STATUS.ERROR
        else:
            return path
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
            return STATUS.ERROR
        else:
            return path
    else:
        path = QFileDialog.getOpenFileName(
            window,
            "请选择文件",
            os.path.dirname(os.path.realpath(sys.argv[0])) +
            "\\bg\\",
            "Image File(*.jpg;*.jpge;*.png;*.bmp);;All File(*.*)"
        )[0]
        if not os.path.isfile(path):
            QMessageBox.critical(
                window,
                "错误",
                "请选择一张图片！",
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Ok
            )
            return STATUS.ERROR
        else:
            return path


def getPhoto(path: str, window):
    try:
        file = open(path, 'rb')
        img = base64.b64encode(file.read())
        file.close()
        return img
    except Exception as e:
        QMessageBox.critical(
            window,
            "错误",
            "无法打开文件！\n错误信息"+str(e.args),
            QMessageBox.StandardButton.Ok,
            QMessageBox.StandardButton.Ok
        )
        return STATUS.ERROR


def getPhotoFromPath(path: str, window) -> list[list[str] | list[bytes]] | Literal[STATUS.ERROR]:
    img_list_list: list[str] = []
    img_base64_list: list[bytes] = []
    if os.path.isdir(path):
        for file in os.listdir(path):
            if file.split(".")[-1] in ["jpg", "jpge", "png", "bmp"]:
                img_list_list.append(file)
                temp = getPhoto(path+"\\"+file, window)
                if temp == STATUS.ERROR:
                    return STATUS.ERROR
                img_base64_list.append(temp)
        if len(img_list_list) == 0:
            QMessageBox.critical(window, "错误", "请选择一个有图片的文件夹！",
                                 QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return STATUS.ERROR
        else:
            return [img_list_list, img_base64_list]
    else:
        QMessageBox.critical(window, "错误", "请选择一个文件夹！",
                             QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
        return STATUS.ERROR


def getAccessToken(client_id: str, client_secret: str, window) -> str | Literal[STATUS.CANCEL]:
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
            QMessageBox.StandardButton.Cancel,  # type: ignore
            QMessageBox.StandardButton.Retry
        )
        if msg == QMessageBox.StandardButton.Retry:
            return getAccessToken(client_id, client_secret, window)
        else:
            return STATUS.CANCEL
    if response and (not ("error_msg" in response.json())):
        access_token: str = response.json()["access_token"]
        return access_token
    else:
        msg = QMessageBox.critical(
            window,
            "错误",
            "请求失败!服务异常,请稍后重试。",
            QMessageBox.StandardButton.Retry |
            QMessageBox.StandardButton.Cancel,  # type: ignore
            QMessageBox.StandardButton.Retry
        )
        if msg == QMessageBox.StandardButton.Retry:
            return getAccessToken(client_id, client_secret, window)
        else:
            return STATUS.CANCEL


def hasProp(obj: dict, prop: Any) -> bool:
    try:
        obj[prop]
        return True
    except Exception:
        return False


def getDistinguishResult(base64_photo: bytes, access_token: str, window, db: ImageData) -> dict | Literal[STATUS.CANCEL]:
    db_data = db.getResultFromImage(base64_photo)
    if db_data != STATUS.NOTFOUND:
        return db_data
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
            QMessageBox.StandardButton.Cancel,  # type: ignore
            QMessageBox.StandardButton.Retry
        )
        if msg == QMessageBox.StandardButton.Retry:
            return getDistinguishResult(base64_photo, access_token, window, db)
        else:
            return STATUS.CANCEL
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
            QMessageBox.StandardButton.Cancel,  # type: ignore
            QMessageBox.StandardButton.Retry
        )
        print(response.json())
        if msg == QMessageBox.StandardButton.Retry:
            return getDistinguishResult(base64_photo, access_token, window, db)
        else:
            return STATUS.CANCEL


def resultParser(result: dict, window) -> list[list] | Literal[STATUS.ERROR]:
    try:
        result_len = len(result["results"])
        result_list = []
        for i in range(result_len):
            temp_text = result["results"][i]["words"]["word"]
            temp_text = temp_text.split("=")
            if len(temp_text) != 2:
                QMessageBox.critical(
                    window,
                    "错误",
                    "请确定图片内只有题目!",
                    QMessageBox.StandardButton.Ok,
                    QMessageBox.StandardButton.Ok
                )
                return STATUS.ERROR
            temp_print = temp_text[0]
            temp_handwriting = temp_text[1]
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
        return STATUS.ERROR


def resultsParser(results: list, window) -> list[list[list[Any]]] | Literal[STATUS.ERROR]:
    results_:list[list[list]] = []
    for i in results:
        result = resultParser(i, window)
        if result != STATUS.ERROR:
            results_.append(result)
        else:
            return STATUS.ERROR
    return results_


def getMode(window) -> Literal[0, 1, 2]:
    msg = QMessageBox(QMessageBox.Icon.Question,
                      "请选择口算图片打开方式", "请选择口算图片打开方式", parent=window)
    file_btn = msg.addButton(window.tr("打开文件"), QMessageBox.ButtonRole.YesRole)
    dir_btn = msg.addButton(window.tr("打开文件夹"), QMessageBox.ButtonRole.NoRole)
    cancel_btn = msg.addButton(
        "取消", QMessageBox.ButtonRole.RejectRole)
    msg.setEscapeButton(cancel_btn)
    msg.exec_()
    if msg.clickedButton() == file_btn:
        return 0
    elif msg.clickedButton() == dir_btn:
        return 1
    else:
        return 2


def saveResult(result: list, mode: int, window, path: Optional[str] = None) -> Literal[STATUS.OK, STATUS.ERROR]:
    if mode == 0:
        path = QFileDialog.getSaveFileName(
            window,
            "请选择保存路径",
            os.path.dirname(os.path.realpath(sys.argv[0])) +
            "\\" +
            path.split(".")[0] +  # type: ignore
            "-" +
            time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) +
            ".csv",
            "CSV File(*.csv);;All File(*.*)"
        )[0]
    elif mode == 1:
        path = QFileDialog.getExistingDirectory(
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
        return STATUS.ERROR
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
            return STATUS.OK
        except PermissionError:
            QMessageBox.critical(
                window,
                "错误",
                "权限不足！",
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Ok
            )
            return STATUS.ERROR
        except Exception as e:
            QMessageBox.critical(
                window,
                "错误",
                "未知错误！\n错误信息"+str(e.args),
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Ok
            )
            return STATUS.ERROR
    else:
        for i in range(0, len(result)):
            try:
                name: str = path[i]
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
                    "权限不足或文件已被占用！",
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
        return STATUS.OK


def found_upgrade(window):
    try:
        url = Values.update_url + "info"
        response = requests.get(url)
        response_json: dict = response.json()
        if Values.version != response_json["version"]:
            msg = QMessageBox(QMessageBox.Icon.Question, "有可用更新", "有可用更新,\n最新版本为" +
                              response_json["version"]+",\n是否安装更新?", parent=window)
            ok_btn = msg.addButton(
                "是", QMessageBox.ButtonRole.AcceptRole)
            cancel_btn = msg.addButton(
                "否", QMessageBox.ButtonRole.RejectRole)
            msg.setDefaultButton(ok_btn)
            msg.setEscapeButton(cancel_btn)
            msg.exec_()
            if msg.clickedButton() == ok_btn:
                os.execv(os.path.dirname(os.path.realpath(
                    sys.argv[0]))+"\\Updater.exe", ("_",))
            else:
                return STATUS.CANCEL
        else:
            QMessageBox.information(
                window, "", "你使用的是最新版", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return STATUS.CANCEL
    except:
        QMessageBox.warning(
            window, "", "检查更新失败", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
        return STATUS.ERROR


def download_updater(window):
    try:
        has_updater = os.path.isfile(os.path.dirname(os.path.realpath(
            sys.argv[0]))+"\\Updater.exe")
        has_upgrade = os.path.isfile(os.path.dirname(os.path.realpath(
            sys.argv[0]))+"\\Upgrade.exe")
        if (not has_updater) and (not has_upgrade):
            response = requests.get(
                Values.update_url+"Updater.exe", allow_redirects=True)
            updater = open(os.path.dirname(os.path.realpath(
                sys.argv[0]))+"\\Updater.exe", "wb")
            updater.write(response.content)
            updater.close()

        if has_upgrade:
            os.rename(os.path.dirname(os.path.realpath(
                sys.argv[0]))+"\\Upgrade.exe", os.path.dirname(os.path.realpath(sys.argv[0]))+"\\Updater.exe")
        return STATUS.OK
    except:
        QMessageBox.critical(
            window, "", "无法下载更新器", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
        return STATUS.ERROR
