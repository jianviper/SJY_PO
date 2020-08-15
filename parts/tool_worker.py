#!/usr/bin/env python
#coding:utf-8
from parts.tool_page import *
from selenium.webdriver.common.action_chains import ActionChains
from common.ws_client import ws_add
import pyautogui, os


def public_getElSize(PO, el):  #获取元素的尺寸
    '''{"height":100,"width":200}'''
    p_list = []
    if PO.find_elements(*el):
        for e in PO.find_elements(*el):
            p_list.append(e.size)
        return p_list


def public_getElPosition(PO, el):  #获取元素位置
    '''{"x":222,"y":333}'''
    p_list = []
    if PO.find_elements(*el):
        for e in PO.find_elements(*el):
            p_list.append(e.location)
        return p_list


def public_getAttrs(PO, el, attr_name):
    if PO.find_element(*el):
        idList = []
        for e in PO.find_elements(*el):
            id = e.get_attribute(attr_name)
            idList.append(id)
        return idList


def get_selectPosition(PO, el):
    #获取设置指定元素的选取范围
    x, y = [], []
    if type(el) == list and len(el) > 0:
        for e in el:
            if PO.find_element(*e):
                for ee in PO.find_elements(*e):
                    x.append(ee.location['x'])
                    y.append(ee.location['y'])
    else:
        if PO.find_element(*el):
            for ee in PO.find_elements(*el):
                x.append(ee.location['x'])
                y.append(ee.location['y'])
    # print('*****\r\n', x, y, '\r\n*******\r\n')
    return ((min(x) - 20, min(y) - 20), (max(x) + 20, max(y) + 20))
    # return (PO.find_element(*el).location, PO.find_element(*el).location_once_scrolled_into_view)


def selection(PO, el):
    '''根据需求多选元素'''
    sleep(1)
    action = ActionChains(PO.driver)
    SP = get_selectPosition(PO, el)
    print("selectPoi:{0}".format(SP))
    header = (By.CLASS_NAME, 'header_fix')
    action.move_to_element_with_offset(PO.find_element(*header), SP[0][0], SP[0][1])
    action.click_and_hold()
    action.move_to_element_with_offset(PO.find_element(*header), SP[1][0], SP[1][1])
    action.release().perform()
    sleep(1)


def public_addTool(PO, toolEL, checkEL, num=1, **kwargs):
    '''登录，新建项目，进入项目添加工具'''
    x, y, margin, height = 200, 150, 0, 0  #初始位置
    header_loc = (By.CSS_SELECTOR, '.header.ant-layout-header')
    if kwargs.get('x') and kwargs.get('y'):
        x, y = kwargs.get('x', 200), kwargs.get('y', 10)
    for i in range(num):
        PO.find_element(*toolEL).click()
        if i > 0:  #添加了一个元素之后
            size = public_getElSize(PO, checkEL)[i - 1]
            height, margin = size['height'], 50
        left_click(PO, x, y + (height + margin) * i, el=header_loc)
        sleep(1)
        left_click(PO, 50, 100, header_loc)
        assert public_check(PO, checkEL)


def public_add(PO, els, **kwargs):
    '''通过websocket添加元素'''
    #els的格式:[("text",1),("img",2),("folder",2)]
    x, y, margin, height = kwargs.get('x', 200), kwargs.get('y', 150), 50, 0  #初始位置
    type = None
    for el in els:
        el_height = 0
        #根据类型设置元素高度
        if el[0] == "t":
            type = "TEXT_LABEL_ADD"
            el_height = 60
        elif el[0] == "i":
            type = "IMAGE_LABEL_ADD"
            el_height = 150
        elif el[0] == 'f':
            type = "CANVAS_ADD"
            el_height = 100
        for i in range(el[1]):
            ws_add(PO, type, x, y)
            y = y + el_height + margin
            sleep(1)


def left_click(PO, x=0, y=0, el=None):
    '''左键点击，可以指定元素及相对位置进行'''
    # print('x:{0},y:{1}'.format(x, y))
    action = ActionChains(PO.driver)
    if x and y and el:  #在指定元素的相对位置
        action.move_to_element_with_offset(PO.find_element(*el), x, y).click().perform()
    elif x and y:  #在当前鼠标位置的相对偏移位置
        action.move_by_offset(x, y).click().perform()
    elif el:  #在指定元素上
        print('cccc')
        # PO.find_element(*el).click()
        action.click(PO.find_element(*el)).perform()
    sleep(1.5)


def rightClick_action(PO, x=0, y=0, el=None, actionEl=None):
    '''右键点击,可以指定元素及其相对位置，也可右键菜单操作'''
    action = ActionChains(PO.driver)
    if x and y and el:  #在指定元素的相对位置
        if el == (By.CLASS_NAME, 'menu_item'):
            x = 700
        action.move_to_element_with_offset(PO.find_element(*el), x, y).context_click().perform()
    elif el:  #在指定元素上
        action.context_click(PO.find_element(*el)).perform()
    else:  #在鼠标当前位置
        action.context_click().perform()
    sleep(1.0)
    if actionEl:
        PO.find_element(*actionEl).click()
        sleep(1.5)


def click_trash(PO):  #打开废纸篓
    tool_recovery_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(9)')
    tips_loc = (By.CLASS_NAME, 'ant-notification-close-x')
    if PO.find_element(*tips_loc, waitsec=2):
        PO.driver.refresh()
    PO.find_element(*tool_recovery_loc).click()


def recovery(PO):
    '''恢复删除的元素'''
    el_trashEL_loc = (By.CSS_SELECTOR, '.item_list>li')
    tool_mouse_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(1)')

    if PO.find_elements(*el_trashEL_loc):
        for el in PO.find_elements(*el_trashEL_loc):
            el.click()
            sleep(0.5)
    PO.find_element(*tool_mouse_loc).click()


def elDrag(PO, start, end):  #拖动元素到某个元素上
    sleep(1)
    action = ActionChains(PO.driver)
    print("aaaaa")
    action.drag_and_drop(PO.find_element(*start), PO.find_element(*end)).perform()
    sleep(1)
    # left_click(PO, 200, -200, end)
    # sleep(2)
    # action.move_by_offset(30, 0).release().perform()
    # action.drag_and_drop_by_offset(PO.find_element(*start),50,0).perform()


def drag_and_drop(PO):
    PO.driver.set_script_timeout(20)
    jq_url = 'https://libs.baidu.com/jquery/2.1.4/jquery.min.js'
    with open('../parts/jquery_loader_helper.js') as f:
        load_jquery_js = f.read()
        # print(load_jquery_js)
    with open('../parts/drag_and_drop_helper.js') as f:
        drag_and_drop_js = f.read()
        # print(drag_and_drop_js)

    PO.driver.execute_async_script(load_jquery_js, jq_url)
    print('gogogo')
    PO.driver.execute_script(
        drag_and_drop_js + '$(".relation_bottom").simulateDragDrop({"dropTarget":".img"});')


def public_textInput(PO, text):
    #文本便签利用JS进行赋值
    js = '''
        document.querySelector('.work_text.work_element').style.border='5px solid red';
        document.getElementsByClassName("text_content")[0].append('{0}');'''.format(text)
    jss = '''
        var ds=document.getElementsByClassName('text_content'); 
        for(i=0;i<ds.length;i++){
            ds[i].parentNode.style.border='3px solid red';
            ds[i].append("%s");
        }
        ''' % text
    PO.driver.execute_script(jss)
    if len(PO.find_elements(*PO.el_textNote_loc)) > 0:
        header_loc = (By.CSS_SELECTOR, '.header.ant-layout-header')
        for e in PO.find_elements(*PO.el_textNote_loc):
            e.click()
            sleep(1)
            left_click(PO, 50, 100, header_loc)


def do_revoke(PO, step=1):
    btn_revoke_loc = (By.CSS_SELECTOR, '.actionImg.backImg')
    sleep(1)
    step = step
    while (step > 0):
        if PO.find_element(*btn_revoke_loc):
            PO.find_element(*btn_revoke_loc).click()
            step -= 1
            sleep(1)


def do_recovery(PO, step=1):
    btn_recovery_loc = (By.CSS_SELECTOR, '.actionImg.restImg')
    sleep(1)
    step = step
    while (step > 0):
        if PO.find_element(*btn_recovery_loc):
            PO.find_element(*btn_recovery_loc).click()
            step -= 1
            sleep(1)


def public_revoke(PO, el=None, **kwargs):
    '''撤销，恢复'''
    if kwargs.get('type') == 'input':  #文本便签的输入
        el_textContent_loc = (By.CSS_SELECTOR, '.work_text.work_element>.text_content')
        do_revoke(PO, kwargs.get('step', 1))  #撤销
        for el in PO.find_elements(*el_textContent_loc):
            assert el.text == ''
        do_recovery(PO, kwargs.get('step', 1))  #恢复
        for el in PO.find_elements(*el_textContent_loc):
            assert el.text != ''
    elif kwargs.get('type') == 'del':  #元素删除
        do_revoke(PO, kwargs.get('step', 1))
        assert public_check(PO, el) != None
        do_recovery(PO, kwargs.get('step', 1))
        assert public_check(PO, el) == None
    elif kwargs.get('type') == 'cut':  #元素剪切
        do_revoke(PO, kwargs.get('step', 1))
        if len(kwargs.get('poi_src')) > 1:  #当有多个元素的时候
            for poi in public_getElPosition(PO, el):
                assert poi in kwargs.get('poi_src')
        else:
            assert public_getElPosition(PO, el) == kwargs.get('poi_src')
        do_recovery(PO, kwargs.get('step', 1))
        if len(kwargs.get('poi_dst')) > 1:  #当有多个元素的时候
            for poi in public_getElPosition(PO, el):
                assert poi in kwargs.get('poi_dst')
        else:
            assert public_getElPosition(PO, el) == kwargs.get('poi_dst')
    elif kwargs.get('type') == 'copy':  #元素复制
        do_revoke(PO, kwargs.get('step', 1))
        assert len(PO.find_elements(*el)) == kwargs.get('num')
        do_recovery(PO, kwargs.get('step', 1))
        assert len(PO.find_elements(*el)) == kwargs.get('num') * 2
    elif kwargs.get('type') == 'rotate' or kwargs.get('type') == 'origin':
        #图片便签的旋转或原图尺寸
        do_revoke(PO)
        assert public_getElSize(PO, el) == kwargs.get('size1')
        do_recovery(PO)
        assert public_getElSize(PO, el) == kwargs.get('size2')
    elif kwargs.get('type') == 'cc':  #文件夹修改颜色
        do_revoke(PO, kwargs.get('step', 1))
        assert public_getAttrs(PO, el, 'src')[0] == kwargs.get('src')
        do_recovery(PO, kwargs.get('step', 1))
        assert public_getAttrs(PO, el, 'src')[0] == kwargs.get('dst')
    else:
        do_revoke(PO, kwargs.get('step', 1))
        assert public_check(PO, el) == None
        do_recovery(PO, kwargs.get('step', 1))
        assert public_check(PO, el) != None
