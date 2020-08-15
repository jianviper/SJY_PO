#!/usr/bin/env python
#coding:utf-8
from time import sleep, strftime, localtime
from selenium.webdriver.common.by import By
from common.create_UUID import create_uuid
import re, requests


def project_name():  #生成项目名称
    return 'AT_{0}'.format(strftime("%Y-%m-%d %H:%M:%S", localtime()))


def textNote_Content():  #生成文本便签内容
    return 'AutoTestContent-{0}'.format(strftime("%Y-%m-%d_%H:%M:%S", localtime()))


def forlder_title():  #生成文件夹标题
    return 'F_{0}'.format(strftime("%Y-%m-%d_%H:%M:%S", localtime()))


def wait_tips(PO, el=None):
    loginTips_loc = (By.CSS_SELECTOR, '.ant-message>span>.ant-message-notice')

    i, ele = 0, loginTips_loc
    if el:
        ele = el
    # print('wait_tips')
    while not PO.find_element(*ele, waitsec=2):
        print('wait:{0}'.format(i))
        if i > 5:
            break
        i += 1
        # sleep(1.5)


def public_init(PO, username, password, proName, el=None):
    public_login(PO, username, password)
    public_createProject(PO, proName)
    public_intoProject(PO, el)


def public_login(PO, username, password):
    '''公用登录方法'''
    noPWLogin_loc = (By.CLASS_NAME, 'header_form')
    pwLogin_loc = (By.XPATH, '//*[@class="login_content"]//span')
    username_loc = (By.XPATH, '//*[@class="form_item"][1]/input')
    password_loc = (By.XPATH, '//*[@class="form_item"][2]/input')
    loginSubmit_loc = (By.CLASS_NAME, 'item_submit')

    PO.find_element(*noPWLogin_loc).click()
    PO.find_element(*pwLogin_loc).click()
    PO.find_element(*username_loc).send_keys(username)
    PO.find_element(*password_loc).send_keys(password)
    PO.find_element(*loginSubmit_loc).click()
    # print('点击登录后{0}'.format(strftime("%Y-%m-%d %H:%M:%S", localtime())))
    wait_tips(PO)
    # print('wait后{0}'.format(strftime("%Y-%m-%d %H:%M:%S", localtime())))
    update_log(PO)
    # print('更新提示{0}'.format(strftime("%Y-%m-%d %H:%M:%S", localtime())))
    bind(PO)
    # print('绑定弹窗{0}'.format(strftime("%Y-%m-%d %H:%M:%S", localtime())))


def public_logout(PO):
    sleep(2)
    menu_user = (By.CSS_SELECTOR, '.menu_user.mouse_hover')
    btn_logout = (By.CSS_SELECTOR, '.meny_level2>li:last-child')

    PO.find_element(*menu_user).click()
    PO.find_element(*btn_logout).click()
    sleep(3)


def public_createProject(PO, name):
    '''公用创建项目'''
    sleep(1)
    createProject_loc = (By.CSS_SELECTOR, '.sure-btn.submit-info')
    projectName_loc = (By.CSS_SELECTOR, '.form-line.iteminput')
    CPSubmitButton_loc = (By.CSS_SELECTOR, '.add_footer>.sure-btn.submit-info')

    PO.find_element(*createProject_loc).click()
    PO.find_element(*projectName_loc).send_keys(name)
    PO.find_element(*CPSubmitButton_loc).click()
    wait_tips(PO)
    sleep(2)


def public_intoProject(PO, el=None):
    lastProject_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:last-child>.item_text')
    work_tool = (By.CLASS_NAME, 'work_tool')
    if el:
        lastProject_loc = el
    PO.find_element(*lastProject_loc).click()
    assert PO.find_element(*work_tool, waitsec=5)


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


def update_log(PO):  #更新日志弹窗
    update_log_loc = (By.CLASS_NAME, 'log_content')
    el_item_loc = (By.CLASS_NAME, 'box_item')
    btn_close_loc = (By.CLASS_NAME, 'header_close')
    btn_more_loc = (By.CLASS_NAME, 'box_more')

    if PO.find_element(*update_log_loc, waitsec=3):
        PO.find_element(*btn_more_loc).click()
        sleep(2)
        assert public_check(PO, el_item_loc, islen=True) > 1
        PO.find_element(*btn_close_loc).click()
        sleep(1)


def bind(PO):  #绑定弹窗
    btn_closeBind_loc = (By.CLASS_NAME, 'closeBtn')
    if PO.find_element(*btn_closeBind_loc, waitsec=3):
        PO.find_element(*btn_closeBind_loc).click()


def public_check(PO, el, text=None, islen=False, attr=None):
    '''公用检查方法，检查元素的文本是否一致，元素是否存在，元素的个数'''
    if text:
        if PO.find_elements(*el, waitsec=3, check='【check】'):
            for e in PO.find_elements(*el, waitsec=3, check='【check】'):
                if e.text != text:
                    return False
            return True
    elif islen:  #返回个数
        result = PO.find_elements(*el, waitsec=3, check='【check】')
        if result:
            return len(result)
        else:
            return 0
    elif attr:  #检查是否有属性值
        return get_attrs(PO, el, attr)
    else:
        return PO.find_element(*el, waitsec=5, check='【check】')


def public_tearDown(PO, url, hurl, username, password):
    if PO.driver.title == '比幕鱼 - 体验': return True
    if PO.driver.title == '比幕鱼 - 注册登录':
        public_login(PO, username, password)
    PO.driver.get(hurl)
    if public_check(PO, (By.CLASS_NAME, 'item_text'), islen=True) > 2:
        public_delProject(PO, hurl, flag=True)


def get_attrs(PO, el, attr_name):
    if PO.find_element(*el):
        idList = []
        for e in PO.find_elements(*el):
            id = e.get_attribute(attr_name)
            idList.append(id)
        return idList
    return 0


def quickReg(PO, host):
    reg_url = 'http://{0}:8080/hetaoNoteApi/app/user/quickReg'.format(host)
    resp_text = requests.post(reg_url, {'uuid': create_uuid()}).text.replace('null', '""')
    data = eval(resp_text)
    url = 'http://{0}/test?id={1}&workId={2}&use=true&name=体验'.format(host,
                                                                      data['user']['workspaces'][0]['canvasId'],
                                                                      data['user']['workspaces'][0]['id'])
    # print(url)
    PO.driver.add_cookie({'name': 'token', 'value': data['token']})
    return url


def tiyan(PO):  #进入体验模式
    btn_skip_loc = (By.CLASS_NAME, 'button_skip')
    el_divs_loc = (By.CSS_SELECTOR, '.work_element')
    el_home_loc = (By.CLASS_NAME, 'home_title')
    host = re.search(r'(\w+\.){2}\w+', PO.driver.current_url).group()

    if host == 'app.bimuyu.tech':
        tiyan_loc = (By.CLASS_NAME, 'content_login')
        PO.driver.get('http://bimuyu.tech/')
        PO.find_element(*tiyan_loc).click()
    else:
        # url = quickReg(PO, host)
        while (PO.driver.title not in ['比幕鱼 - 体验', '比幕鱼 - 体验项目']):
            url = 'http://{0}/login?uuid={1}'.format(host, create_uuid())
            PO.driver.get(url)
            sleep(3)
    wait_tips(PO, PO.tool_loc)
    # print(PO.driver.title)
    # assert '比幕鱼 - 体验' == PO.driver.title
    sleep(1)
    PO.find_element(*btn_skip_loc).click()  #点击跳过教程按钮
    assert len(PO.find_elements(*el_divs_loc)) == 11
    #到home页，新建项目
    if host == 'app.bimuyu.tech':
        PO.find_element(*el_home_loc).click()
    else:
        PO.driver.get('http://{0}/home'.format(host))
    public_createProject(PO, project_name())
    public_intoProject(PO)
