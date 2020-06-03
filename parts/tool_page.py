#!/usr/bin/env python
#coding:utf-8
from time import sleep, strftime, localtime
from selenium.webdriver.common.by import By


def project_name():  #生成项目名称
    return 'AT_{0}'.format(strftime("%Y-%m-%d %H:%M:%S", localtime()))


def textNote_Content():  #生成文本便签内容
    return '自动化测试文本-{0}'.format(strftime("%Y-%m-%d %H:%M:%S", localtime()))


def wait_tips(PO, el=None):
    loginTips_loc = (By.XPATH, '//*[@class="ant-message"]/span//span')

    i, ele = 0, loginTips_loc
    if el:
        ele = el
    # print('wait_tips')
    while not PO.find_element(*ele, waitsec=1.5):
        print('wait:{0}'.format(i))
        if i > 5:
            break
        i += 1
        # sleep(1.5)


def public_init(PO, username, password, proName, el=None):
    public_login(PO, username, password)
    public_createProject(PO, proName)
    public_intoProject(PO, el)


def public_login(PO, username, password, bind=False):
    '''公用登录方法'''
    noPWLogin_loc = (By.CLASS_NAME, 'header_form')
    pwLogin_loc = (By.XPATH, '//*[@class="login_content"]//span')
    username_loc = (By.XPATH, '//*[@class="form_item"][1]/input')
    password_loc = (By.XPATH, '//*[@class="form_item"][2]/input')
    loginSubmit_loc = (By.CLASS_NAME, 'item_submit')
    win_bind_loc = (By.CLASS_NAME, 'ant-modal-body')
    btn_closeBind_loc = (By.CLASS_NAME, 'closeBtn')

    PO.find_element(*noPWLogin_loc).click()
    PO.find_element(*pwLogin_loc).click()
    PO.find_element(*username_loc).send_keys(username)
    PO.find_element(*password_loc).send_keys(password)
    PO.find_element(*loginSubmit_loc).click()
    wait_tips(PO)
    if not bind:
        if public_check(PO, win_bind_loc):
            print('close bind')
            PO.find_element(*btn_closeBind_loc).click()
    sleep(2)


def public_logout(PO):
    sleep(2)
    menu_user = (By.CSS_SELECTOR, '.menu_user.mouse_hover')
    btn_logout = (By.CSS_SELECTOR, '.meny_level2>li:last-child')

    PO.find_element(*menu_user).click()
    PO.find_element(*btn_logout).click()
    sleep(3)


def public_createProject(PO, name):
    '''公用创建项目'''
    createProject_loc = (By.CSS_SELECTOR, '.sure-btn.submit-info')
    projectName_loc = (By.CSS_SELECTOR, '.form-line.iteminput')
    CPSubmitButton_loc = (By.CSS_SELECTOR, '.add_footer>.sure-btn.submit-info')

    sleep(1)
    PO.find_element(*createProject_loc).click()
    PO.find_element(*projectName_loc).send_keys(name)
    PO.find_element(*CPSubmitButton_loc).click()
    wait_tips(PO)
    sleep(2)


def public_intoProject(PO, el=None):
    lastProject_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:last-child>.item_text')
    if el:
        lastProject_loc = el
    PO.find_element(*lastProject_loc).click()
    sleep(2)


def public_delProject(PO, home_url, flag=True):
    '''公用删除项目'''
    if not flag:
        return
    sleep(3)
    lastProjectMenu_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:last-child>.item_set')
    delMenuButton_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:last-child>ul>:last-child')
    delProjectName_loc = (By.CSS_SELECTOR, '.header_subtitle>span')
    inputProjectName_loc = (By.CSS_SELECTOR, '.form_item>input[type=text]')
    delSubmitButton_loc = (By.CSS_SELECTOR, '.add_footer>.sure-btn.submit-info')

    PO.driver.get(home_url)
    PO.find_element(*lastProjectMenu_loc).click()
    PO.find_element(*delMenuButton_loc).click()
    PO.find_element(*inputProjectName_loc).send_keys(PO.find_element(*delProjectName_loc).text)
    PO.find_element(*delSubmitButton_loc).click()
    sleep(1)


def public_check(PO, el, text=None, islen=False, attr=None):
    '''公用检查方法，检查元素的文本是否一致，元素是否存在，元素的个数'''
    if text:
        if PO.find_elements(*el, waitsec=3, check='【check】'):
            for e in PO.find_elements(*el, waitsec=3, check='【check】'):
                if e.text != text:
                    return False
            return True
    elif islen:
        return len(PO.find_elements(*el, waitsec=3, check='【check】'))
    elif attr:  #检查是否有属性值
        for i in get_attrs(PO, el, attr):
            if not i:
                return False
        return True
    else:
        return PO.find_element(*el, waitsec=3, check='【check】')


def public_tearDown(PO, url, hurl, username, password):
    if PO.driver.title == '比幕鱼 - 注册登录':
        public_login(PO, username, password)
    PO.driver.get(hurl)
    if public_check(PO, (By.CLASS_NAME, 'item_text'), islen=True) > 2:
        public_delProject(PO, hurl, flag=True)


def get_attrs(PO, el, attr_name):
    if PO.find_elements(*el):
        idList = []
        for e in PO.find_elements(*el):
            id = e.get_attribute(attr_name)
            idList.append(id)
        return idList
