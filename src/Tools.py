import base64
import csv
import getpass
import os
from sys import argv
import threading
import requests
import win32api
import win32con
import win32ui


def getPhoto() -> bytes:
    dlg = win32ui.CreateFileDialog(1)
    dlg.SetOFNInitialDir("C:\\Users\\" + getpass.getuser() + "\\Desktop\\")
    dlg.DoModal()
    filename: str = dlg.GetPathName()
    if os.path.isfile(filename):
        file = open(filename, 'rb')
        img = base64.b64encode(file.read())
        file.close()
        return img
    else:
        win32api.MessageBox(0, "请选择一张图片！", "", win32con.MB_OK)


def getAccessToken(client_id: str, client_secret: str) -> str:
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + \
        client_id+'&client_secret='+client_secret
    response = requests.get(host)
    if response:
        access_token = response.json()["access_token"]
        return access_token
    else:
        retry = win32api.MessageBox(
            0, "请求失败!请检查是否连接因特网后重试。", "", win32con.MB_RETRYCANCEL)
        if retry == 4:
            return getAccessToken()
        else:
            return False


def hasProp(obj: dict, prop: str):
    try:
        temp = obj[prop]
        del temp
        return True
    except Exception:
        return False


def getDistinguishResult(base64_photo: bytes, access_token: str) -> dict:
    host = "https://aip.baidubce.com/rest/2.0/ocr/v1/doc_analysis"
    params = {"image": base64_photo,
              "language_type": "CHN_ENG", "result_type": "big"}
    host = host + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(host, data=params, headers=headers)
    if response and (not ("error_msg" in response)):
        result = response.json()
        return result
    else:
        retry = win32api.MessageBox(
            0, "请求失败!请检查是否连接因特网后重试。", "", win32con.MB_RETRYCANCEL)
        if retry == 4:
            return getDistinguishResult()
        else:
            return False


def resultParser(result: dict) -> list:
    try:
        result_len = len(result["results"])
    except:
        print("无法获取识别结果!")
        print(result)
        return False

    result_list = []
    for i in range(result_len):
        temp_text: str = result["results"][i]["words"]["word"]
        temp_text = temp_text.split("=")
        if len(temp_text) != 2:
            win32api.MessageBox(0, "请确定图片内只有题目!", "", win32con.MB_OK)
            return False
        temp_print: str = temp_text[0]
        temp_handwriting: str = temp_text[1]
        temp_handwriting = float(eval(temp_handwriting.replace("/", "1")))
        temp_1 = temp_print
        temp_1.replace("×", "*")
        temp_1.replace("x", "*")
        temp_1.replace("÷", "/")
        temp_answer = float(eval(temp_1))
        temp_right = "✓" if (float(temp_handwriting) == temp_answer) else "✗"
        temp_print.replace("*", "×")
        temp_print.replace("/", "÷")
        temp_result = [temp_print, temp_handwriting, temp_answer, temp_right]
        result_list.append(temp_result)
    return result_list


def saveResult(result: list) -> None:
    dlg = win32ui.CreateFileDialog(0)
    dlg.SetOFNInitialDir("C:\\Users\\" + getpass.getuser() + "\\Desktop\\")
    dlg.DoModal()
    path: str = dlg.GetPathName()
    try:
        result_file = open(path, "w", encoding="utf-8")
        writer = csv.writer(result_file)
        writer.writerow(["题目", "学生答案", "正确答案", "对错"])
        for one in result:
            writer.writerow(one)
        result_file.close()
        win32api.MessageBox(0, "已保存至"+path, "结果保存成功!", win32con.MB_OK)
    except PermissionError:
        win32api.MessageBox(0, "权限不足!", "", win32con.MB_OK)
    except:
        pass
