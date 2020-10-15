#!/usr/bin/env python
#coding:utf-8
from time import sleep, strftime, localtime, time
from selenium.webdriver.common.by import By
from common.create_UUID import create_uuid
from common.BasePage import BasePage
import re, requests

'''
summary:页面的公用方法
'''


class PageTool():

    def __init__(self, po):
        self.po = po
        pass

    def project_name(self) -> str:  #生成项目名称
        return 'AT_{0}'.format(strftime("%Y-%m-%d %H:%M", localtime()))

    def textNote_Content(self):  #生成文本便签内容
        return 'AutoTestContent-{0}'.format(strftime("%Y-%m-%d_%H:%M:%S", localtime()))

    def forlder_title(self):  #生成文件夹标题
        return 'F_{0}'.format(strftime("%Y-%m-%d_%H:%M:%S", localtime()))

    def wait_tips(self, el=None, sec=2, max=5):
        Tips_loc = (By.CSS_SELECTOR, '.ant-message>span>.ant-message-notice')

        i, ele = 0, Tips_loc
        if el:
            ele = el
        # print('wait_tips')
        while not self.po.find_element(*ele, waitsec=sec):
            print('wait:{0}'.format(i))
            if i > max:
                break
            i += 1
            # sleep(1.5)

    def public_init(self, username, password, proName, el=None):
        self.public_login(username, password)
        self.public_createProject(proName)
        self.public_intoProject(el)

    def public_login(self, username, password):
        '''公用登录方法'''
        noPWLogin_loc = (By.CLASS_NAME, 'header_form')
        pwLogin_loc = (By.XPATH, '//*[@class="login_content"]//span')
        username_loc = (By.XPATH, '//*[@class="form_item"][1]/input')
        password_loc = (By.XPATH, '//*[@class="form_item"][2]/input')
        loginSubmit_loc = (By.CLASS_NAME, 'item_submit')

        self.po.find_element(*noPWLogin_loc).click()
        self.po.find_element(*pwLogin_loc).click()
        self.po.find_element(*username_loc).send_keys(username)
        self.po.find_element(*password_loc).send_keys(password)
        self.po.find_element(*loginSubmit_loc).click()
        # print('点击登录后{0}'.format(strftime("%Y-%m-%d %H:%M:%S", localtime())))
        self.wait_tips()
        # print('wait后{0}'.format(strftime("%Y-%m-%d %H:%M:%S", localtime())))
        self.check_updateLog()
        # print('更新提示{0}'.format(strftime("%Y-%m-%d %H:%M:%S", localtime())))
        self.check_bind()
        # print('绑定弹窗{0}'.format(strftime("%Y-%m-%d %H:%M:%S", localtime())))

    def public_logout(self):
        sleep(2)
        menu_user = (By.CSS_SELECTOR, '.menu_user.mouse_hover')
        btn_logout = (By.CSS_SELECTOR, '.meny_level2>li:last-child')

        self.po.find_element(*menu_user).click()
        self.po.find_element(*btn_logout).click()
        sleep(3)

    def public_createProject(self, name):
        '''公用创建项目'''
        sleep(1)
        createProject_loc = (By.CSS_SELECTOR, '.sure-btn.submit-info.creatWork')
        projectName_loc = (By.CSS_SELECTOR, '.form-line.iteminput')
        from random import randint
        randint = randint(1, 4)
        pic_loc = (By.CSS_SELECTOR, '.picList>div:nth-child({0})'.format(randint))
        SubmitButton_loc = (By.CSS_SELECTOR, '.add_footer.modal_foot>:last-child>.sure-btn.submit-info')

        self.po.find_element(*createProject_loc).click()
        self.po.find_element(*projectName_loc).send_keys(name)
        self.po.find_element(*pic_loc).click()
        self.po.find_element(*SubmitButton_loc).click()
        self.wait_tips()
        sleep(2)

    def public_intoProject(self, el=None):
        # lastProject_loc = (By.CSS_SELECTOR, '.home_content>:last-child>.item_text')
        firstProject_loc = (By.CSS_SELECTOR, '.home_content>:first-child>.item_text')
        yuqun_loc = (By.CLASS_NAME, 'yuqun')
        yqclose_loc = (By.CSS_SELECTOR, '.planC_header>.header_close')
        work_tool = (By.CLASS_NAME, 'work_tool')
        if el:
            firstProject_loc = el
        self.po.find_element(*firstProject_loc).click()
        assert self.po.find_element(*work_tool)
        if self.po.find_element(*yuqun_loc):  #关闭鱼群计划
            self.po.find_element(*yqclose_loc).click()

    def public_delProject(self, home_url=None, flag=True):
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
            self.po.driver.get(home_url)
        from selenium.webdriver.common.action_chains import ActionChains
        action = ActionChains(self.po.driver)
        action.move_to_element(self.po.find_element(*firstPro_loc)).perform()
        sleep(1.5)
        self.po.find_element(*firstProMenu_loc).click()
        self.po.find_element(*btn_del_loc).click()
        self.po.find_element(*input_proName_loc).send_keys(self.po.find_element(*text_proName_loc).text)
        self.po.find_element(*btn_delSubmit_loc).click()
        sleep(1)

    def check_updateLog(self, skip=True):  #更新日志弹窗
        update_log_loc = (By.CLASS_NAME, 'log_content')
        el_item_loc = (By.CLASS_NAME, 'box_item')
        btn_close_loc = (By.CSS_SELECTOR, '.content_header>.header_close')
        btn_more_loc = (By.CLASS_NAME, 'box_more')

        if self.po.find_element(*update_log_loc, waitsec=3):
            if skip:  #直接关闭日志
                # p_time = strftime("%Y-%m-%d-%H_%M_%S", localtime(time()))
                # self.po.driver.get_screenshot_as_file('E:\\python\\project\\SJY_PO\\screen\\{0}.jpg'.format(p_time))
                self.po.find_element(*btn_close_loc).click()
            else:  #测试下加载更多
                self.po.find_element(*btn_more_loc).click()
                sleep(2)
                assert self.public_check(el_item_loc, islen=True) > 1
                self.po.find_element(*btn_close_loc).click()
                sleep(1)

    def check_bind(self):  #绑定弹窗
        btn_closeBind_loc = (By.CLASS_NAME, 'closeBtn')
        if self.po.find_element(*btn_closeBind_loc, waitsec=3):
            self.po.find_element(*btn_closeBind_loc).click()

    def get_attrs(self, el, attr_name, **kwargs):
        attrList = []
        if kwargs.get('driver'):
            if self.po.driver.find_element_by_css_selector(el):
                for e in self.po.driver.find_elements_by_css_selector(el):
                    attr = e.get_attribute(attr_name)
                    if attr:
                        attrList.append(attr)
        else:
            if self.po.find_element(*el):
                for e in self.po.find_elements(*el):
                    attr = e.get_attribute(attr_name)
                    if attr:
                        attrList.append(attr)
        return attrList

    def public_check(self, el, text=None, islen=False, attr=None, **kwargs):
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
            if self.po.find_elements(*el, waitsec=3, check='【check】'):
                for e in self.po.find_elements(*el, waitsec=3, check='【check】'):
                    if e.text != text:
                        return False
                return True
        elif islen:  #返回个数
            if kwargs.get('driver'):
                sleep(3)
                return len(self.po.driver.find_elements_by_css_selector(el))
                # return len(self.po.driver.find_elements_by_xpath(el))
            else:
                return len(self.po.find_elements(*el, waitsec=3, check='【check】'))
        elif attr:  #检查是否有属性值
            return self.get_attrs(el, attr, driver=kwargs.get('driver'))
        else:
            if kwargs.get("driver"):
                return self.po.driver.find_element_by_css_selector(el)
            else:
                return self.po.find_element(*el, waitsec=5, check='【check】')

    def public_tearDown(self, url, hurl, username, password):
        if self.po.driver.title == '比幕鱼 - 体验': return True
        if self.po.driver.title == '比幕鱼 - 注册登录':
            self.public_login(username, password)
        if self.po.driver.title != '比幕鱼 - 白板列表':
            self.po.driver.get(hurl)
        if self.public_check((By.CLASS_NAME, 'item_text'), islen=True) > 2:
            while (self.public_check((By.CLASS_NAME, 'item_text'), islen=True) > 2):
                self.public_delProject(hurl, flag=True)

    def quickReg(self, host):
        reg_url = 'http://{0}:8080/hetaoNoteApi/app/user/quickReg'.format(host)
        resp_text = requests.post(reg_url, {'uuid': create_uuid()}).text.replace('null', '""')
        data = eval(resp_text)
        url = 'http://{0}/test?id={1}&workId={2}&use=true&name=体验'.format(host,
                                                                          data['user']['workspaces'][0]['canvasId'],
                                                                          data['user']['workspaces'][0]['id'])
        # print(url)
        self.po.driver.add_cookie({'name': 'token', 'value': data['token']})
        return url

    def tiyan(self):  #进入体验模式
        btn_skip_loc = (By.CLASS_NAME, 'button_skip')
        el_divs_loc = (By.CSS_SELECTOR, '.work_element')
        el_home_loc = (By.CLASS_NAME, 'home_title')
        tool_loc = (By.CSS_SELECTOR, 'work_tool')
        host = re.search(r'(\w+\.){2}\w+', self.po.driver.current_url).group()

        if host == 'app.bimuyu.tech':
            tiyan_loc = (By.CLASS_NAME, 'content_login')
            self.po.driver.get('http://bimuyu.tech/')
            self.po.find_element(*tiyan_loc).click()
        else:
            # url = quickReg(PO, host)
            print(self.po.driver.title)
            count = 0
            while (self.po.driver.title not in ['比幕鱼 - 体验', '比幕鱼 - 体验项目']):
                if count > 3: raise Exception('go to tiyan fail!')
                count += 1
                url = 'http://{0}/login?uuid={1}'.format(host, create_uuid())
                self.po.driver.get(url)
                sleep(3)
        self.public_check(tool_loc)
        # print(self.po.driver.title)
        # assert '比幕鱼 - 体验' == self.po.driver.title
        sleep(1)
        if self.po.find_element(*btn_skip_loc):
            self.po.find_element(*btn_skip_loc).click()  #点击跳过教程按钮
        assert len(self.po.find_elements(*el_divs_loc)) == 11
        #到home页，新建项目
        if host == 'app.bimuyu.tech':
            self.po.find_element(*el_home_loc).click()
        else:
            self.po.driver.get('http://{0}/home'.format(host))
        self.public_createProject(self.project_name())
        self.public_intoProject()

    def el_click(self, el):
        sleep(1)
        if self.po.find_element(*el):
            return self.po.find_element(*el).click()
        else:
            assert Exception("function get_text() 元素不存在!")

    def get_text(self, el, type=None):
        sleep(1)
        if self.po.find_element(*el):
            if not type:
                return self.po.find_element(*el).text
            else:
                return self.po.find_element(*el).get_attribute('value')
        else:
            assert Exception("function get_text() 元素不存在!")
