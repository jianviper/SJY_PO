#!/usr/bin/env python
#coding:utf-8
from websocket import create_connection
from parts.tool_page import get_attrs
from common.get_config import get, get_ws
from time import sleep
from selenium.webdriver.common.by import By
import re, time, json, requests, random


def ws_creat(PO):  #生成websocket
    token = PO.driver.get_cookie('token')['value']
    url = PO.driver.current_url
    canvasId = re.search(r'(id=)\d+', url).group().split('=')[1]
    url = get_ws()  #wss://test.api.bimuyu.tech/api/echo
    wsUrl = url + '?token={0}&canvasId={1}'.format(token, canvasId)
    ws = create_connection(wsUrl)
    return ws


def add_ws(PO, type, poix, poiy, **kwargs):
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
    ws = kwargs.get('ws', ws_creat(PO))
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


def get_last(PO):
    els = PO.find_elements(*(By.CSS_SELECTOR, '.work_element'))
    sleep(2)
    if els:
        print(len(els))
    else:
        print('fail')


def get_ID(PO):  #通过接口获取新增元素的id
    host = get('host', 'host')
    url = "https://{0}.bimuyu.tech/api/app/id/get".format(host)
    token = PO.driver.get_cookie('token')['value']
    data = {"size": 1}
    header = {"Content-Type": "application/x-www-form-urlencoded", 'token': token}
    resp = requests.post(url, data, headers=header, verify=False)
    el_id = eval(resp.text)["list"][0]
    return el_id


if __name__ == '__main__':
    ids = ['86359', '86361']
    pos = [{'x': 200, 'y': 150}, {'x': 200, 'y': 350}]
