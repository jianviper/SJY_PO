#!/usr/bin/env python
#coding:utf-8
from time import sleep
from selenium.webdriver.common.by import By
import os
from unittest import TestCase


def wait_tips(pageObject, el=None):
    loginTips_loc = (By.XPATH, '//*[@class="ant-message"]/span//span')

    i = 0
    ele = loginTips_loc
    if el:
        ele = el
    print('wait_tips')
    while not pageObject.find_element(*ele):
        print('wait:{0}'.format(i))
        if i > 6:
            break
        i += 1
        sleep(1.5)


def public_login(pageObject, username, password, bind=False):
    '''公用登录方法'''
    noPWLogin_loc = (By.CLASS_NAME, 'header_form')
    pwLogin_loc = (By.XPATH, '//*[@class="login_content"]//span')
    username_loc = (By.XPATH, '//*[@class="form_item"][1]/input')
    password_loc = (By.XPATH, '//*[@class="form_item"][2]/input')
    loginSubmit_loc = (By.CLASS_NAME, 'item_submit')
    win_bind_loc = (By.CLASS_NAME, 'ant-modal-body')
    btn_closeBind_loc = (By.CLASS_NAME, 'closeBtn')

    # pageObject.open()
    pageObject.find_element(*noPWLogin_loc).click()
    pageObject.find_element(*pwLogin_loc).click()
    pageObject.find_element(*username_loc).send_keys(username)
    pageObject.find_element(*password_loc).send_keys(password)
    pageObject.find_element(*loginSubmit_loc).click()
    wait_tips(pageObject)
    if not bind:
        if public_check(pageObject, win_bind_loc):
            print('close bind')
            pageObject.find_element(*btn_closeBind_loc).click()
    sleep(3)


def public_logout(pageObject):
    sleep(3)
    menu_user = (By.CSS_SELECTOR, '.menu_user.mouse_hover')
    btn_logout = (By.CSS_SELECTOR, '.meny_level2>li:last-child')

    pageObject.find_element(*menu_user).click()
    pageObject.find_element(*btn_logout).click()
    sleep(3)


def public_createProject(pageObject, name):
    '''公用创建项目'''
    createProject_loc = (By.CSS_SELECTOR, '.header_add.ant-btn')
    projectName_loc = (By.CLASS_NAME, 'ant-input')
    CPSubmitButton_loc = (By.CSS_SELECTOR, '.sure-btn.ant-btn')

    pageObject.find_element(*createProject_loc).click()
    pageObject.find_element(*projectName_loc).send_keys(name)
    pageObject.find_element(*CPSubmitButton_loc).click()
    sleep(2)


def public_intoProject(pageObject):
    lastProject_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:last-child>.item_text')

    pageObject.find_element(*lastProject_loc).click()
    sleep(2)


def public_delProject(pageObject, home_url):
    '''公用删除项目'''
    lastProjectMenu_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:last-child>.item_set>img')
    delMenuButton_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:last-child>ul>:last-child')
    delProjectName_loc = (By.CSS_SELECTOR, '.header_subtitle>span')
    inputProjectName_loc = (By.CSS_SELECTOR, '.form_item>input[type=text]')
    delSubmitButton_loc = (By.CSS_SELECTOR, '.sure-btn.ant-btn')

    pageObject.driver.get(home_url)
    pageObject.find_element(*lastProjectMenu_loc).click()
    pageObject.find_element(*delMenuButton_loc).click()
    pageObject.find_element(*inputProjectName_loc).send_keys(pageObject.find_element(*delProjectName_loc).text)
    pageObject.find_element(*delSubmitButton_loc).click()
    sleep(1)


def public_getSize(pageObject, el):
    return pageObject.find_element(*el).size


def public_addTool(pageObject, toolEL, checkEL, nums=1, action=None):
    '''登录，新建项目，进入项目添加工具'''
    x, y, margin, height = 200, 150, 0, 0
    tc = TestCase()
    for i in range(nums):
        pageObject.choose_tool(toolEL)
        if i > 0:  #添加了一个元素之后
            size = public_getSize(pageObject, checkEL)
            height, margin = size['height'], 50
        pageObject.action_click(x, y + height + margin, el=pageObject.svg_loc)
        tc.assertTrue(public_check(pageObject, checkEL))
        if action == 'upload':  #需要上传图片
            pageObject.find_elements(*checkEL)[i].click()
            sleep(1)
            os.system('uploadIMG.exe')
            sleep(5)


def public_check(pageObject, el, text=None, islen=False):
    '''公用检查方法，检查元素的文本是否一致，元素是否存在，元素的个数'''
    if text:
        for e in pageObject.find_elements(*el, waitsec=5, check='【check】'):
            if e.text != text:
                return False
        return True
    elif islen:
        return len(pageObject.find_elements(*el, waitsec=5, check='【check】'))
    else:
        return pageObject.find_element(*el, waitsec=3, check='【check】')

# def public_rdXY()
