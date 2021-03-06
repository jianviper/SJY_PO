#!/usr/bin/env python
#coding:utf-8
import sys
from time import sleep, strftime, localtime
from selenium.webdriver.common.by import By
from common.create_UUID import create_uuid
import re, requests

'''
summary:页面的公用方法
'''


def project_name():  #生成项目名称
    #AT_2020-7-16 16:44:26
    return 'AT_{0}'.format(strftime("%Y-%m-%d_%H:%M", localtime()))


def text_Content():  #生成文本便签内容
    return 'AutoTestContent-{0}'.format(strftime("%Y-%m-%d_%H:%M:%S", localtime()))


def folder_title():  #生成文件夹标题
    return 'F_{0}'.format(strftime("%Y-%m-%d_%H:%M:%S", localtime()))


def wait_tips(PO, el=None, sec=2, max=5):
    Tips_loc = (By.CSS_SELECTOR, '.ant-message>span>.ant-message-notice')
    i, ele = 0, Tips_loc
    if el:
        ele = el
    while not PO.find_element(*ele, waitsec=2):
        print('wait:{0}'.format(i))
        if i > max:
            break
        i += 1


def wait_text(PO, el=None, text=''):
    i = 0
    while i < 10:
        if str(PO.find_element(*el).text).replace(' ', ''):
            # print('wait_text:{0}'.format(PO.find_element(*el).text))
            break
        i += 1
        sleep(1)


def cooperation(po: list, **kwargs):
    '''
    协作测试
    :param po:
    :param kwargs:
    :return:
    '''
    #获取浏览器最大化尺寸
    width = po[0].driver.get_window_size().get("width")
    height = po[0].driver.get_window_size().get("height")
    #设置两个浏览器分屏1:1尺寸
    po[0].set_w_size(width / 2 + 4, height)
    po[0].set_w_poi(0, 0)
    po[1].set_w_size(width / 2 + 4, height)
    po[1].set_w_poi(width / 2 - 4, 0)
    #初始化浏览器页面
    public_init(po[0], 14500000050, 123456, kwargs.get('pro_name', project_name()))
    public_login(po[1], 14500000051, 123456)
    join_invite(po)  #进入协作


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
    print('点击登录后{0}'.format(strftime("%Y-%m-%d %H:%M:%S", localtime())))
    wait_tips(PO)
    # print('wait后{0}'.format(strftime("%Y-%m-%d %H:%M:%S", localtime())))
    #check_updateLog(PO)
    # print('更新提示{0}'.format(strftime("%Y-%m-%d %H:%M:%S", localtime())))
    #check_bind(PO)
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
    createProject_loc = (By.CSS_SELECTOR, '.sure-btn.submit-info.creatWork')
    projectName_loc = (By.CSS_SELECTOR, '.form-line.iteminput')
    from random import randint
    randint = randint(1, 4)
    pic_loc = (By.CSS_SELECTOR, '.picList>div:nth-child({0})'.format(randint))
    SubmitButton_loc = (By.CSS_SELECTOR, '.add_footer.modal_foot>:last-child>.sure-btn.submit-info')

    PO.find_element(*createProject_loc).click()
    PO.find_element(*projectName_loc).send_keys(name)
    PO.find_element(*pic_loc).click()
    PO.find_element(*SubmitButton_loc).click()
    wait_tips(PO)
    sleep(2)


def public_intoProject(PO, el=None):
    # lastProject_loc = (By.CSS_SELECTOR, '.home_content>:last-child>.item_text')
    firstProject_loc = (By.CSS_SELECTOR, '.home_content>:first-child>.item_text')
    yuqun_loc = (By.CLASS_NAME, 'yuqun')
    yqclose_loc = (By.CSS_SELECTOR, '.planC_header>.header_close')
    work_tool = (By.CLASS_NAME, 'work_tool')
    if el: firstProject_loc = el
    PO.find_element(*firstProject_loc).click()
    assert PO.find_element(*work_tool)
    # if PO.find_element(*yuqun_loc, waitsec=3):  #关闭鱼群计划
    #     PO.find_element(*yqclose_loc).click()


def public_delProject(PO, home_url=None, flag=True):
    '''公用删除项目'''
    if not flag:
        return
    sleep(3)
    firstPro_loc = (By.CSS_SELECTOR, '.home_content>:first-child')
    firstProMenu_loc = (By.CSS_SELECTOR, '.home_content>:first-child>.item_set')
    # lastProjectMenu_loc = (By.CSS_SELECTOR, '.home_content>:last-child>.item_set')
    btn_del_loc = (By.CSS_SELECTOR, '.footBtn.delBtn')
    text_proName_loc = (By.CSS_SELECTOR, '.header_subtitle>span')
    input_proName_loc = (By.CSS_SELECTOR, '.form_item>input[type=text]')
    btn_delSubmit_loc = (By.CSS_SELECTOR, '.add_footer>.sure-btn.submit-info')

    if home_url:
        PO.driver.get(home_url)
    from selenium.webdriver.common.action_chains import ActionChains
    action = ActionChains(PO.driver)
    action.move_to_element(PO.find_element(*firstPro_loc)).perform()
    sleep(1)
    PO.find_element(*firstProMenu_loc).click()
    PO.find_element(*btn_del_loc).click()
    PO.find_element(*input_proName_loc).send_keys(PO.find_element(*text_proName_loc).text)
    PO.find_element(*btn_delSubmit_loc).click()
    sleep(1)


def check_updateLog(PO, skip=True):  #更新日志弹窗
    update_log_loc = (By.CLASS_NAME, 'log_content')
    el_item_loc = (By.CLASS_NAME, 'box_item')
    btn_close_loc = (By.CSS_SELECTOR, '.content_header>.header_close')
    btn_more_loc = (By.CLASS_NAME, 'box_more')

    if PO.find_element(*update_log_loc, waitsec=3):
        if skip:  #直接关闭日志
            # p_time = strftime("%Y-%m-%d-%H_%M_%S", localtime(time()))
            # PO.driver.get_screenshot_as_file('E:\\python\\project\\SJY_PO\\screen\\{0}.jpg'.format(p_time))
            PO.find_element(*btn_close_loc).click()
        else:  #测试下加载更多
            PO.find_element(*btn_more_loc).click()
            sleep(2)
            assert public_check(PO, el_item_loc, islen=True) > 1
            PO.find_element(*btn_close_loc).click()
            sleep(1)


def check_bind(PO):  #绑定弹窗
    btn_closeBind_loc = (By.CLASS_NAME, 'closeBtn')
    if PO.find_element(*btn_closeBind_loc, waitsec=3):
        PO.find_element(*btn_closeBind_loc).click()


def get_attrs(PO, el, attr_name, **kwargs):
    '''
    获取元素的属性值
    :param el:
    :param attr_name:属性名称
    :param kwargs: driver:True使用原生元素定位
    :return:
    '''
    attrList = []
    if kwargs.get('driver'):
        if PO.driver.find_element_by_css_selector(el):
            for e in PO.driver.find_elements_by_css_selector(el):
                attr = e.get_attribute(attr_name)
                if attr:
                    attrList.append(attr)
    else:
        if PO.find_element(*el):
            for e in PO.find_elements(*el):
                attr = e.get_attribute(attr_name)
                if attr:
                    attrList.append(attr)
    return attrList


def public_check(PO, el, text=None, islen=False, attr=None, **kwargs):
    '''
    公用检查方法，检查元素的文本是否一致，元素是否存在，元素的个数
    :param PO:
    :param el: 要检查的元素
    :param text: 元素的文本
    :param islen: 返回元素的数量
    :param attr: 返回元素的属性值
    :param kwargs:driver:使用原始找元素的方法
    :return:
    '''
    if text:
        for e in PO.find_elements(*el, waitsec=3, check='【checks】'):
            if e.text != text:
                return False
        return True
    elif islen:  #返回个数
        if kwargs.get('driver'):
            sleep(3)
            return len(PO.driver.find_elements_by_css_selector(el))
            # return len(PO.driver.find_elements_by_xpath(el))
        else:
            return len(PO.find_elements(*el, waitsec=3, check='【checks】'))
    elif attr:  #检查是否有属性值
        return get_attrs(PO, el, attr, driver=kwargs.get('driver'))
    else:
        if kwargs.get("driver"):
            return PO.driver.find_element_by_css_selector(el)
        else:
            return PO.find_element(*el, waitsec=kwargs.get('sec', 5), check='【check】')


def public_tearDown(PO, url, home_url, username, password):
    if type(PO) != list:
        PO = [PO]
    for po in PO:
        if po.driver.title == '比幕鱼 - 体验': return True
        if po.driver.title == '比幕鱼 - 注册登录':
            public_login(po, username, password)
        if po.driver.title != '比幕鱼 - 白板列表':
            po.driver.get(home_url)
        if public_check(po, (By.CLASS_NAME, 'item_text'), islen=True) > 2:
            while (public_check(po, (By.CLASS_NAME, 'item_text'), islen=True) > 2):
                public_delProject(po, home_url, flag=True)


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
    tool_loc = (By.CSS_SELECTOR, 'work_tool')
    host = re.search(r'(\w+\.){2}\w+', PO.driver.current_url).group()

    if host == 'app.bimuyu.tech':
        tiyan_loc = (By.CLASS_NAME, 'buttons_signup')
        PO.driver.get('http://bimuyu.tech/')
        PO.find_element(*tiyan_loc).click()
    else:
        # url = quickReg(PO, host)
        print(PO.driver.title)
        count = 0
        while (PO.driver.title not in ['比幕鱼 - 体验', '比幕鱼 - 体验项目']):
            if count > 3: raise Exception('go to tiyan fail!')
            count += 1
            url = 'http://{0}/login?uuid={1}'.format(host, create_uuid())
            PO.driver.get(url)
            sleep(3)
    public_check(PO, tool_loc)
    # assert '比幕鱼 - 体验' == PO.driver.title
    sleep(1)
    if PO.find_element(*btn_skip_loc):
        PO.find_element(*btn_skip_loc).click()  #点击跳过教程按钮
    assert len(PO.find_elements(*el_divs_loc)) == 11
    #到home页，新建项目
    if host == 'app.bimuyu.tech':
        PO.find_element(*el_home_loc).click()
    else:
        PO.driver.get('http://{0}/home'.format(host))
    public_createProject(PO, project_name())
    public_intoProject(PO)


def el_click(PO, el):
    sleep(1)
    if PO.find_element(*el):
        PO.find_element(*el).click()
        sleep(1)
    else:
        assert Exception("function get_text() 元素不存在!")


def get_text(PO, el, type=None):
    '''
    获取元素文本
    :param PO:
    :param el:
    :param type:True通过属性获取，False直接获取text
    :return:
    '''
    sleep(1)
    if PO.find_element(*el):
        if not type:
            return PO.find_element(*el).text
        else:
            return PO.find_element(*el).get_attribute('value')
    else:
        assert Exception("function get_text() 元素不存在!")


def get_screenshot(PO, filename='title'):
    try:
        PO.driver.save_screenshot('..\\screen\\{0}.png'.format(filename))
    except BaseException as e:
        print(e)


def join_invite(po: list):
    '''
    加入邀请
    :param po: po（浏览器）列表
    :param project_name: 白板名称
    :return:
    '''
    el_click(po[0], (By.CLASS_NAME, 'userout'))
    inviUrl = po[0].find_element(*(By.ID, 'inviUrl')).get_attribute('value')
    # print(inviUrl)
    po[1].driver.get(inviUrl)
    wait_text(po[1], (By.CSS_SELECTOR, '.invitation_content>p>span:last-child'))  #等待白板名称显示
    el_click(po[1], (By.CSS_SELECTOR, '.invitation_submit.sure-btn'))  #点击加入邀请
    assert public_check(po[1], po[1].tool_loc)
