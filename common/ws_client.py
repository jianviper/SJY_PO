#!/usr/bin/env python
#coding:utf-8
from websocket import create_connection
from parts.tool_page import get_attrs
from common.get_config import get
from time import sleep
from selenium.webdriver.common.by import By
import re, time, json, requests, random


def ws_creatClient(token, canvasId):
    url = get('websocket', 'ws')
    wsUrl = url + '?token={0}&canvasId={1}'.format(token, canvasId)
    ws = create_connection(wsUrl)
    return ws


def ws_creat(PO):
    token = get_token(PO)
    url = PO.driver.current_url
    canvasId = re.search(r'(id=)\d+', url).group().split('=')[1]
    url = get('websocket', 'ws')
    wsUrl = url + '?token={0}&canvasId={1}'.format(token, canvasId)
    ws = create_connection(wsUrl)
    return ws


def ws_add(PO, type, poix, poiy, **kwargs):
    # token = get_token(PO)
    url = PO.driver.current_url
    canvasId = re.search(r'(id=)\d+', url).group().split('=')[1]
    # ws = ws_creatClient(token, canvasId)
    ws = kwargs.get('ws')
    img_url = ["https://hetao-note.oss-cn-hangzhou.aliyuncs.com/16217/5CxWGwys5aZdEwTfaNrFzTmx2pcz2njp.png",
               "https://hetao-note.oss-cn-hangzhou.aliyuncs.com/16217/cm3ANpMCi36zsBe8kb6bacdsPEsZCyrH.jpg",
               "https://hetao-note.oss-cn-hangzhou.aliyuncs.com/16217/s5X2dCphQkzc3WPtrBSix5cxjt4W776K.png",
               "https://hetao-note.oss-cn-hangzhou.aliyuncs.com/16217/HhRpT45GBDxJdey7bQC4dkBPEmNkYpfp.png"]
    send_msg = {
        "canvasId": canvasId,
        "poiX": poix,
        "poiY": poiy,
        "status": "edit",
        "id": get_ID(PO),
    }
    color_list = ['#508ceb', '#71c846', '#dd4a4a', '#ffd14d', '#666d77']
    try:
        #组织发送数据,根据类型加入数据
        if type == "TEXT_LABEL_ADD":
            utime = time.strftime('%Y-%m-%d %H:%M:%S')
            send_msg.update(
                {"type": "TEXT_LABEL_ADD", "content": 'AutoTestContent-{0}'.format(utime), "poiW": 350, "poiH": 60})
        elif type == "IMAGE_LABEL_ADD":
            send_msg.update({"type": "IMAGE_LABEL_ADD",
                             "img": img_url[random.randint(0, 3)],
                             "transform": 0,
                             "poiW": 350,
                             "poiH": 150,
                             })
        elif type == "CANVAS_ADD":
            send_msg.update({"type": "CANVAS_ADD",
                             "name": "标题",
                             "bgColor": color_list[random.randint(0, 4)]})
        elif type == 'FILE_LABEL_ADD':
            fileId = None
            if 'test' in url:
                fileId = '32486103420375040'
            elif 'app' in url:
                fileId = '32543435433054208'
            send_msg = {"type": "FILE_LABEL_ADD", "id": get_ID(PO), "fileId": fileId, "poiX": poix,
                        "poiY": poiy, "title": "websocket.docx"}
        # print(send_msg)
        # print('{0}__send_msg:{1}'.format(type, send_msg))
        ws.send(json.dumps(send_msg))  #执行发送
    except BaseException as e:
        print(e)


def WSupload_img(PO, el, attr_name):
    token = get_token(PO)
    url = PO.driver.current_url
    # poi = public_getElPosition(PO, el)
    poi = []
    el_id = get_attrs(PO, el, attr_name)
    #url = 'https://app.bimuyu.tech/work?id=81115&workId=20639&name=22'
    canvasId = re.search(r'(id=)\d+', url).group().split('=')[1]
    ws = ws_creatClient(token, canvasId)
    img_url = ["https://hetao-note.oss-cn-hangzhou.aliyuncs.com/16217/5CxWGwys5aZdEwTfaNrFzTmx2pcz2njp.png",
               "https://hetao-note.oss-cn-hangzhou.aliyuncs.com/16217/cm3ANpMCi36zsBe8kb6bacdsPEsZCyrH.jpg",
               "https://hetao-note.oss-cn-hangzhou.aliyuncs.com/16217/s5X2dCphQkzc3WPtrBSix5cxjt4W776K.png",
               "https://hetao-note.oss-cn-hangzhou.aliyuncs.com/16217/HhRpT45GBDxJdey7bQC4dkBPEmNkYpfp.png"]
    try:
        for i in range(len(el_id)):
            utime = time.strftime('%Y-%m-%d %H:%M:%S')
            #组织发送数据
            send_msg = {"type": "DEAL_EDIT", "type2": 2, "canvasId": canvasId, "elementId": el_id[i], "isEdit": 1,
                        "status": "edit", "imgurl": img_url[i % 4], "html": img_url[i % 4], "update": utime,
                        "move": False,
                        "poiX": poi[i].get('x'), "poiY": poi[i].get('y'), "sizeW": 350, "sizeH": 150}
            # print(send_msg)
            ws.send(json.dumps(send_msg))  #执行发送
            time.sleep(1.5)
    finally:
        ws.close()


'''
def get_last_el(PO):
    text_el = (By.CSS_SELECTOR, '.work_text.work_element')
    img_el = (By.CSS_SELECTOR, '.work_image.work_element')
    folder_el = (By.CSS_SELECTOR, '.work_file.work_element')

    if PO.find_element(*text_el):
        poi = public_getElPosition(PO, text_el)
        size = public_getElSize(PO, text_el)
        print('text\r\n', poi, size)
    if PO.find_element(*img_el):
        poi = public_getElPosition(PO, img_el)
        size = public_getElSize(PO, img_el)
        print('img\r\n', poi, size)
    if PO.find_element(*folder_el):
        poi = public_getElPosition(PO, folder_el)
        size = public_getElSize(PO, folder_el)
        print('folder\r\n', poi, size)
'''


def get_last(PO):
    els = PO.find_elements(*(By.CSS_SELECTOR, '.work_element'))
    sleep(2)
    if els:
        print(len(els))
    else:
        print('fail')


def api_add(PO, type, num=1):
    #已弃用
    #type--1文件夹，2文本，4图片便签
    #url = 'https://app.bimuyu.tech/work?id=81115&workId=20639&name=22'
    url = create_apiUrl(PO)
    token = PO.driver.get_cookies()[1]['value']
    parentId = re.search(r'(id=)\d+', url).group().split('=')[1]

    x, y, margin, height = 200, 150, 50, 0  #初始位置
    for i in range(num):
        if i > 0:  #添加了一个元素之后
            y = 150 + (150 + margin) * i
        data = {'content': '', 'ext': '', 'html': '', 'parentId': parentId, 'position': '{0},{1},350,150'.format(x, y),
                'type': type}
        requests.post(url, data, headers={'token': token}, verify=False)
        sleep(1)
    PO.driver.refresh()
    sleep(2)
    # response = requests.post(api_url, data, headers={'token': token}, verify=False)
    # print(response.text)


def create_apiUrl(PO):
    url = PO.driver.current_url
    host = re.search(r'(\w+\.){2}\w+', url).group()
    # print('host:',host)
    api_url = "http://{0}:8080/hetaoNoteApi/app/".format(host)
    if host == 'app.bimuyu.tech':
        api_url = 'https://api.hetaonote.com:8080/hetaoNoteApi/app/'
    elif host == 'pre.bimuyu.tech':
        api_url = 'http://pre.api.bimuyu.tech/hetaoNoteApi/app/'
    return api_url


def get_token(PO):
    cookies = PO.driver.get_cookies()
    token = ''
    for i in cookies:
        for key, value in i.items():
            if value == 'token':
                token = i['value']
    return token


def get_ID(PO):
    url = "{0}id/get".format(create_apiUrl(PO))
    token = get_token(PO)
    data = {"size": 1}
    header = {"Content-Type": "application/x-www-form-urlencoded", 'token': token}
    resp = requests.post(url, data, headers=header, verify=False)
    # print(resp.text)
    el_id = eval(resp.text)["list"][0]
    return el_id


if __name__ == '__main__':
    ids = ['86359', '86361']
    pos = [{'x': 200, 'y': 150}, {'x': 200, 'y': 350}]
