#!/usr/bin/env python
from selenium.webdriver.common.by import By
from common.BasePage import BasePage
from time import sleep
'''
Create on 2020-3-17
author:linjian
summary:所有页面元素定位都在此层定义，UI一旦有更改，只需在修改这一层页面对象属性即可。
'''


#继承BasePage类
class LoginPage(BasePage):
    #定位器，通过元素属性定位元素对象
    pwLogin_loc = (By.XPATH, '//*[@class="login_content"]//span')
    username_loc = (By.XPATH, '//*[@class="form_item"][1]/input')
    password_loc = (By.XPATH, '//*[@class="form_item"][2]/input')
    loginSubmit_loc = (By.CLASS_NAME, 'item_submit')
    loginTips_loc=(By.XPATH,'//*[@class="ant-message"]/span//span')

    #操作
    #通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    #打开网页
    def open(self):
        self._open(self.baseurl)

    def choose_pwLogin(self):
        self.find_element(*self.pwLogin_loc).click()
        sleep(0.5)

    def input_username(self, username):
        self.find_element(*self.username_loc).send_keys(username)

    def input_password(self, password):
        self.find_element(*self.password_loc).send_keys(password)

    def click_submit(self):
        self.find_element(*self.loginSubmit_loc).click()

    def get_loginTips(self):
        return self.find_element(*self.loginTips_loc).text

