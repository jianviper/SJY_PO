#!/usr/bin/env python
#coding:utf-8
from websocket import create_connection
from parts.tool_page import get_attrs
from common.get_config import get
from time import sleep
from selenium.webdriver.common.by import By
import re, time, json, requests, random


def ws_creat(PO):
    token = PO.driver.get_cookie('token')['value']
    url = PO.driver.current_url
    canvasId = re.search(r'(id=)\d+', url).group().split('=')[1]
    url = get('websocket', 'ws')
    wsUrl = url + '?token={0}&canvasId={1}'.format(token, canvasId)
    ws = create_connection(wsUrl)
    return ws


def WS_add(PO, type, poix, poiy, **kwargs):
    '''
    通过websocket添加同步元素
    :param PO:
    :param type: 元素类型
    :param poix: 元素x坐标,默认传进来200
    :param poiy: 元素y坐标,默认传进来150
    :param kwargs:
    :return:
    '''
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
    folder_color = ['#508ceb', '#71c846', '#dd4a4a', '#ffd14d', '#666d77']
    note_color = ['#fcfca5', '#f9c88f', '#f7a18d', '#9add7c', '#98d3f4', '#998aed']
    try:
        #组织发送数据,根据类型加入数据
        if type == "TEXT_LABEL_ADD":  #文本
            send_msg.update({"type": "TEXT_LABEL_ADD",
                             "content": kwargs.get('text'),
                             "poiW": None,
                             "poiH": 39
                             })
        elif type == "NOTE_LABEL_ADD":  #便签
            send_msg.update({"type": "NOTE_LABEL_ADD",
                             "bgColor": note_color[random.randint(0, 5)],
                             "scale": {"left": 0, "top": 0, "scale": 1, "ex": 0, "yf": 0},
                             "poiW": 200,
                             "poiH": 200,
                             })
        elif type == "IMAGE_LABEL_ADD":  #图片便签
            img = img_url[random.randint(0, 3)]
            send_msg.update({"type": "IMAGE_LABEL_ADD",
                             "img": img,
                             "transform": 0,
                             "poiW": 350,
                             "poiH": 150,
                             "title": img
                             })
        elif type == "CANVAS_ADD":  #文件夹
            send_msg.update({"type": "CANVAS_ADD",
                             "name": "标题",
                             "bgColor": folder_color[random.randint(0, 4)]
                             })
        elif type == 'FILE_LABEL_ADD':  #文件
            fileId = None
            if url.find('test') >= 0:
                fileId = '65181418191458304'
            elif url.find('app') >= 0 or url.find('pre') >= 0:
                fileId = '68441297693839360'
            send_msg.update({"type": "FILE_LABEL_ADD", "fileId": fileId, "title": "websocket.docx"})
        # print(send_msg)
        print('【{0}】:{1}'.format(type, send_msg))
        ws.send(json.dumps(send_msg))  #执行发送
    except BaseException as e:
        print(e)


def WSupload_img(PO, el, attr_name):
    url = PO.driver.current_url
    # poi = public_getElPosition(PO, el)
    poi = []
    el_id = get_attrs(PO, el, attr_name)
    #url = 'https://app.bimuyu.tech/work?id=81115&workId=20639&name=22'
    canvasId = re.search(r'(id=)\d+', url).group().split('=')[1]
    ws = ws_creat(PO)
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


def get_last(PO):
    els = PO.find_elements(*(By.CSS_SELECTOR, '.work_element'))
    sleep(2)
    if els:
        print(len(els))
    else:
        print('fail')


def api_add(PO, type, num=1):
    #####已弃用######
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
    api_url = "https://{0}:8080/hetaoNoteApi/app/".format(host)
    if host == 'app.bimuyu.tech':
        api_url = 'https://api.bimuyu.tech/api/app/'
    elif host == 'pre.bimuyu.tech':
        api_url = 'http://pre.api.bimuyu.tech/hetaoNoteApi/app/'
    return api_url


def get_ID(PO):
    url = "{0}id/get".format(create_apiUrl(PO))
    token = PO.driver.get_cookie('token')['value']
    data = {"size": 1}
    header = {"Content-Type": "application/x-www-form-urlencoded", 'token': token}
    resp = requests.post(url, data, headers=header, verify=False)
    el_id = eval(resp.text)["list"][0]
    return el_id


if __name__ == '__main__':
    ids = ['86359', '86361']
    pos = [{'x': 200, 'y': 150}, {'x': 200, 'y': 350}]
