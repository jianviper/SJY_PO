#!/usr/bin/env python
from common.BasePage import BasePage
from parts.tool_page import *

'''
Create on 2020-3-17
author:linjian
summary:所有页面元素定位都在此层定义，UI一旦有更改，只需在修改这一层页面对象属性即可。
'''


#继承BasePage类
class LoginPage(BasePage):
    #定位器，通过元素属性定位元素对象
    noPWLogin_loc = (By.CLASS_NAME, 'header_form')
    pwLogin_loc = (By.CSS_SELECTOR, '.item_subtitle>span')
    # username_loc = (By.XPATH, '//*[@class="form_item"][1]/input')
    username_loc = (By.XPATH, '//*[@placeholder="手机号"]')
    password_loc = (By.CSS_SELECTOR, '.item_password.form-line')
    verCode_loc=(By.XPATH,'//*[@placeholder="验证码"]')
    # loginSubmit_loc = (By.CLASS_NAME, 'item_submit')
    loginSubmit_loc = (By.CSS_SELECTOR, '.item_submit.sure-btn')
    warnTitle_loc=(By.CLASS_NAME,'warn_title')
    loginTips_loc = (By.XPATH, '//*[@class="ant-message"]/span//span')

    #操作
    #通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    #打开网页
    def open(self):
        self._open(self.baseurl)

    def choose_noPWLogin(self):
        self.find_element(*self.noPWLogin_loc).click()
        sleep(0.5)

    def choose_pwLogin(self):
        self.choose_noPWLogin()
        self.find_element(*self.pwLogin_loc).click()
        sleep(0.5)

    def input_username(self, username):
        self.find_element(*self.username_loc).send_keys(username)

    def input_password(self, password):
        self.find_element(*self.password_loc).send_keys(password)

    def input_verCode(self,Vcode):
        self.find_element(*self.verCode_loc).send_keys(Vcode)

    def click_submit(self):
        self.find_element(*self.loginSubmit_loc).click()

    def get_loginTips(self):
        wait_tips(self)
        return self.find_element(*self.loginTips_loc).text

    def login(self, username, password, flag=0, code=0):
        '''flag是否需要登录成功，code是否用验证码登录'''
        self.open()
        if code == 0:
            self.choose_pwLogin()
            self.input_username(username)
            self.input_password(password)
        else:
            self.choose_noPWLogin()
            self.input_username(username)
            self.input_verCode(password)
        self.click_submit()
        if flag == 1:
            wait_tips(self)
