#!/usr/bin/env python
#coding:utf-8
from websocket import create_connection
from parts.tool_worker import public_getElPosition
from parts.tool_page import get_attrs
import re, time, json


def ws_creatClient(token, canvasId):
    wsUrl = 'wss://api.hetaonote.com:8080/hetaoNoteApi/echo?token={0}&canvasId={1}'.format(token, canvasId)
    ws = create_connection(wsUrl)
    return ws


def WSupload_img(PO, el, attr_name):
    token = PO.driver.get_cookies()[1]['value']
    url = PO.driver.current_url
    poi = public_getElPosition(PO, el)
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
                        "status": "edit", "imgurl": img_url[i], "html": img_url[i], "update": utime, "move": False,
                        "poiX": poi[i].get('x'), "poiY": poi[i].get('y'), "sizeW": 350, "sizeH": 150}
            # print(send_msg)
            ws.send(json.dumps(send_msg))  #执行发送
            time.sleep(1.5)
    finally:
        ws.close()


if __name__ == '__main__':
    ids = ['86359', '86361']
    pos = [{'x': 200, 'y': 150}, {'x': 200, 'y': 350}]
