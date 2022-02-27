import base64
import os
import requests
import win32api
import win32con
import win32ui


def getPhoto() -> bytes:
    dlg = win32ui.CreateFileDialog(1)
    dlg.SetOFNInitialDir('C:/')
    dlg.DoModal()
    filename: str = dlg.GetPathName()
    if os.path.isfile(filename) and filename.split(".")[-1] in ["jpg", "jpge", "png", "bmp"]:
        f = open(filename, 'rb')
        img = base64.b64encode(f.read())
        f.close()
        return img
    else:
        win32api.MessageBox(0, "请选择一张图片！", "", win32con.MB_OK)
        return False


def getAccessToken(client_id: str, client_secret: str) -> str:
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + \
        client_id+'&client_secret='+client_secret
    response = requests.get(host)
    if response:
        access_token = response.json()["access_token"]
        return access_token
    else:
        retry = win32api.MessageBox(
            0, "请求失败！请检查是否连接因特网后重试。", "", win32con.MB_RETRYCANCEL)
        if retry == 4:
            return getAccessToken()
        else:
            return False

def hasProp(obj:dict,prop:str):
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
    if response:
        result = response.json()
        return result
    else:
        retry = win32api.MessageBox(
            0, "请求失败！请检查是否连接因特网后重试。", "", win32con.MB_RETRYCANCEL)
        if retry == 4:
            return getDistinguishResult()
        else:
            return False


def resultParser(distinguish_result: dict) -> list:
    pass
