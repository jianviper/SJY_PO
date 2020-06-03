#!/usr/bin/env python
#coding:utf-8
from parts.tool_page import *
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui, os


def public_getElSize(PO, el):  #获取元素的尺寸
    p_list = []
    if PO.find_elements(*el):
        for e in PO.find_elements(*el):
            p_list.append(e.size)
        return p_list


def public_getElPosition(PO, el):  #获取元素位置
    p_list = []
    if PO.find_elements(*el):
        for e in PO.find_elements(*el):
            p_list.append(e.location)
        return p_list


def public_addTool(PO, toolEL, checkEL, nums=1, action=None, **kwargs):
    '''登录，新建项目，进入项目添加工具'''
    x, y, margin, height = 200, 150, 0, 0  #初始位置
    if kwargs.get('x') and kwargs.get('y'):
        x, y = kwargs.get('x', 200), kwargs.get('y', 150)
    for i in range(nums):
        PO.find_element(*toolEL).click()
        if i > 0:  #添加了一个元素之后
            size = public_getElSize(PO, checkEL)[i - 1]
            height, margin = size['height'], 50
        left_click(PO, x, y + (height + margin) * i, el=PO.svg_loc)
        sleep(1)
        assert public_check(PO, checkEL)
        if action == 'upload':  #需要上传图片
            PO.find_elements(*checkEL)[i].click()
            sleep(1)
            os.system('uploadIMG.exe')
            sleep(5)


def get_selectPosition(PO, el):
    #获取设置指定元素的选取范围
    x, y = [], []
    if type(el) == list and len(el) > 0:
        for e in el:
            for ee in PO.find_elements(*e):
                x.append(ee.location['x'])
                y.append(ee.location['y'])
    else:
        for ee in PO.find_elements(*el):
            x.append(ee.location['x'])
            y.append(ee.location['y'])
    print(x, y)
    return ((min(x) - 20, min(y) - 20), (max(x) + 20, max(y) + 20))
    # return (PO.find_element(*el).location, PO.find_element(*el).location_once_scrolled_into_view)


def selection(PO, el):
    '''根据需求多选元素'''
    SP = get_selectPosition(PO, el)
    sleep(1)
    action = ActionChains(PO.driver)
    action.move_to_element_with_offset(PO.find_element(*PO.svg_loc), SP[0][0], SP[0][1])
    action.click_and_hold().move_by_offset(SP[1][0], SP[1][1]).release().perform()


def left_click(PO, x=0, y=0, el=None):
    '''左键点击，可以指定元素及相对位置进行'''
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
        action.move_to_element_with_offset(PO.find_element(*el), x, y).context_click().perform()
    elif el:  #在指定元素上
        action.context_click(PO.find_element(*el)).perform()
    else:  #在鼠标当前位置
        action.context_click().perform()
    sleep(1.0)
    if actionEl:
        PO.find_element(*actionEl).click()
        sleep(1.5)
    if actionEl == (By.CSS_SELECTOR, '.text_menu>li:nth-child(3)'):  #删除
        wait_tips(PO)


def click_trash(PO):  #打开废纸篓
    tool_recovery_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(9)')

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
