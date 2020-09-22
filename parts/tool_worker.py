#!/usr/bin/env python
#coding:utf-8
from parts.tool_page import *
from selenium.webdriver.common.action_chains import ActionChains
from common.ws_client import ws_add, ws_creat
import pyautogui, os

'''
summary:画布页面的公用方法
'''

header_loc = (By.CSS_SELECTOR, '.header.ant-layout-header')


def public_getElSize(PO, el):  #获取元素的尺寸
    '''{"height":100,"width":200}'''
    p_list = []
    if PO.find_elements(*el):
        for e in PO.find_elements(*el):
            p_list.append(e.size)
        return p_list


def public_getElPosition(PO, el, **kwargs):  #获取元素位置
    '''{"x":222,"y":333}'''
    if kwargs.get('driver'):
        find = PO.driver.find_elements_by_css_selector(el)
    else:
        find = PO.find_elements(*el)
    if find:
        poi_list = []
        for e in find:
            poi_list.append(e.location)
        return poi_list


def public_getAttrs(PO, el, attr_name):
    if PO.find_element(*el):
        idList = []
        for e in PO.find_elements(*el):
            id = e.get_attribute(attr_name)
            idList.append(id)
        return idList


def _get_selectPosition(PO, el):
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
    '''
    根据需求多选元素
    :param PO:
    :param el: 要选择的元素，可以是列表
    :return:
    '''
    sleep(1)
    action = ActionChains(PO.driver)
    SP = _get_selectPosition(PO, el)
    print("selectPoi:{0}".format(SP))
    header = (By.CLASS_NAME, 'header_fix')
    action.move_to_element_with_offset(PO.find_element(*header), SP[0][0], SP[0][1])
    action.click_and_hold()
    action.move_to_element_with_offset(PO.find_element(*header), SP[1][0], SP[1][1])
    action.release().perform()
    sleep(1)


def public_addTool(PO, toolEL, checkEL, num=1, **kwargs):
    '''
    登录，新建项目，进入项目添加工具
    :param PO:
    :param toolEL: 左侧工具栏的工具按钮
    :param checkEL: 添加后生成的元素
    :param num: 添加的元素数量
    :param kwargs: 可传参数x，y设置初始位置
    :return:
    '''
    x, y, margin, height = 200, 150, 0, 0  #初始位置
    # header_loc = (By.CSS_SELECTOR, '.header.ant-layout-header')
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
    '''
    通过websocket添加元素
    :param PO:
    :param els: 需要添加的元素，格式:[("t",1),("i",2),("f",2)]
    t:文本便签，i：图片便签，f：文件夹，file：文件
    :param kwargs: 可传入x，y设置初始位置
    :return:
    '''
    x, y, margin, height = kwargs.get('x', 200), kwargs.get('y', 150), 50, 0  #初始位置
    type = None
    ws = None
    try:
        ws = ws_creat(PO)
        for el in els:
            el_height = 0
            #根据类型设置ws请求类型和元素高度
            if el[0] == "t":
                type = "TEXT_LABEL_ADD"
                el_height = 60
            elif el[0] == "i":
                type = "IMAGE_LABEL_ADD"
                el_height = 150
            elif el[0] == 'f':
                type = "CANVAS_ADD"
                el_height = 100
            elif el[0] == 'file':
                type = 'FILE_LABEL_ADD'
                el_height = 110
            for i in range(el[1]):
                ws_add(PO, type, x, y, ws=ws)  #请求websocket
                y = y + el_height + margin
                sleep(1)
        PO.driver.refresh()
    except BaseException as e:
        print(e)
    finally:
        ws.close()


def left_click(PO, x=0, y=0, el=None):
    '''
    左键点击，可以指定元素及相对位置进行
    :param PO:
    :param x: x偏移量
    :param y: y偏移量
    :param el: 在哪个元素上左键点击
    :return:
    '''
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


def rightClick(PO, x=0, y=0, el=None, actionEl=None):
    '''
    右键点击,可以指定元素及其相对位置，也可右键菜单操作
    :param PO:
    :param x: x偏移量
    :param y: y偏移量
    :param el: 在哪个元素上右键点击
    :param actionEl: 右键菜单的选项
    :return:
    '''
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


def double_click(PO, el):
    #双击元素
    action = ActionChains(PO.driver)
    action.double_click(PO.find_element(*el)).perform()


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


def elDrag(PO, el=None, start=None, end=None):
    '''
    按住某个元素拖动，根据el决定是否拖动到空白处还是某个元素上
    :param PO:
    :param el: 指定从这个元素上拉出关联线
    :param start: 开始元素，有传el代表offset_x
    :param end: 结束元素，有传el代表offset_y
    :return:
    '''
    sleep(1)
    action = ActionChains(PO.driver)
    if el:
        action.drag_and_drop_by_offset(PO.find_element(*el), start, end).perform()
    else:
        action.drag_and_drop(PO.find_element(*start), PO.find_element(*end)).perform()
    sleep(1)


'''
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
'''


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
        # header_loc = (By.CSS_SELECTOR, '.header.ant-layout-header')
        el_textContent_loc = (By.CSS_SELECTOR, '.work_text.work_element>.text_content')
        action = ActionChains(PO.driver)
        for e in PO.find_elements(*el_textContent_loc):
            action.double_click(e).perform()
            sleep(1)
            left_click(PO, 50, 100, header_loc)


def do_revoke(PO, step=1):  #撤销
    btn_revoke_loc = (By.CSS_SELECTOR, '.actionImg.backImg')
    sleep(1)
    step = step
    while (step > 0):
        if PO.find_element(*btn_revoke_loc):
            PO.find_element(*btn_revoke_loc).click()
            step -= 1
            sleep(1)


def do_recovery(PO, step=1):  #恢复
    btn_recovery_loc = (By.CSS_SELECTOR, '.actionImg.restImg')
    sleep(1)
    step = step
    while (step > 0):
        if PO.find_element(*btn_recovery_loc):
            PO.find_element(*btn_recovery_loc).click()
            step -= 1
            sleep(1)


def public_revoke(PO, el=None, **kwargs):
    '''
    撤销，恢复
    :param PO:
    :param el: 被撤销和恢复的元素
    :param kwargs: 可传参数type:操作类型，step:撤销和恢复的步数
    :return:
    '''
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
            poi = public_getElPosition(PO, el, driver=kwargs.get('driver'))
            assert len(kwargs.get('poi_src')) == len(poi)
            for p in poi:
                assert p in kwargs.get('poi_src')
        else:
            assert public_getElPosition(PO, el, driver=kwargs.get('driver')) == kwargs.get('poi_src')
        do_recovery(PO, kwargs.get('step', 1))
        if len(kwargs.get('poi_dst')) > 1:  #当有多个元素的时候
            poi = public_getElPosition(PO, el, driver=kwargs.get('driver'))
            assert len(kwargs.get('poi_dst')) == len(poi)
            for p in poi:
                assert p in kwargs.get('poi_dst')
        else:
            assert public_getElPosition(PO, el, driver=kwargs.get('driver')) == kwargs.get('poi_dst')
    elif kwargs.get('type') == 'copy':  #元素复制
        do_revoke(PO, kwargs.get('step', 1))
        if kwargs.get('driver'):
            assert len(PO.driver.find_elements_by_css_selector(el)) == kwargs.get('num')
        else:
            assert len(PO.find_elements(*el)) == kwargs.get('num')
        do_recovery(PO, kwargs.get('step', 1))
        if kwargs.get('driver'):
            assert len(PO.driver.find_elements_by_css_selector(el)) == kwargs.get('num') * 2
        else:
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
    else:  #元素添加的撤销和恢复
        do_revoke(PO, kwargs.get('step', 1))
        assert public_check(PO, el) == None
        do_recovery(PO, kwargs.get('step', 1))
        assert public_check(PO, el) != None


def elAddLine(PO, start=None, end=None):
    '''
    两个元素之间新建关联线
    :param PO:
    :param start: 起始元素的关联线节点
    :param end: 终止元素,已定位
    :return:
    '''
    sleep(1)
    action = ActionChains(PO.driver)
    action.drag_and_drop(PO.find_element(*start), end).perform()
    sleep(1)


def addWithLine(PO, els, start=None, end=None):
    '''
    添加元素，且加上关联线
    :param PO:
    :param els: 要添加的元素
    :param start: 起始元素
    :param end: 结束元素
    :return:
    '''
    btn_relbtm_loc = (By.CLASS_NAME, 'relation_bottom')
    public_add(PO, els)
    if start and end:  #如果多个不同的元素
        PO.find_element(*start).click()
        elAddLine(PO, btn_relbtm_loc, PO.find_element(*end))
    elif start:  #同一种元素
        el_list = PO.find_elements(*start)
        if el_list:
            for i in range(len(el_list)):
                el_list[0].click()
                elAddLine(PO, btn_relbtm_loc, el_list[1])
        else:
            raise Exception("页面中未找到{0}元素".format(start))
    left_click(PO, 80, 100, header_loc)
