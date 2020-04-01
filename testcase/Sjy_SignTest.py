#!/usr/bin/env python
import unittest, time
from pages.Page_login import LoginPage
from parts.login_ps import login
'''
Create on 2020-3-17
author:linjian
summary:使用unittest框架编写测试用例
'''


class LoginTest(unittest.TestCase):
    def setUp(self):
        url = 'https://app.bimuyu.tech/login'
        self.username = '14500000000'
        self.username_format_error='145000'
        self.password = '111111'
        self.password_error='999999'
        self.password_format_error='123'
        self.loginpage = LoginPage(base_url=url)

    def tearDown(self):
        self.loginpage.driver.quit()

    #用例执行体
    def test_sign(self):
        '''正确的账号密码登录'''
        #声明signpage对象
        #执行具体操作
        login(self.loginpage,self.username,self.password,1)
        self.assertEqual('比幕鱼 - 项目列表',self.loginpage.driver.title)

    def test_phone_format_error(self):
        '''使用格式错误的手机号登录'''
        login(self.loginpage,self.username_format_error,self.password)
        self.assertEqual('请填写正确的手机号',self.loginpage.get_loginTips())

    def test_password_error(self):
        '''使用错误的密码登录'''
        login(self.loginpage,self.username,self.password_error)
        self.assertEqual('账号或密码错误',self.loginpage.get_loginTips())

    def test_password_format_error(self):
        '''使用格式错误的密码登录'''
        login(self.loginpage,self.username,self.password_format_error)
        self.assertEqual('密码（6-15位数字和字母）',self.loginpage.get_loginTips())

    def test_CodeLogin_noCode(self):
        '''未填写验证码的情况下进行登录'''
        login(self.loginpage, self.username, '',code=1)
        self.assertEqual('失败',self.loginpage.get_loginTips())

    def test_CodeLogin_errorCode(self):
        '''使用错误的验证码的进行登录'''
        login(self.loginpage, self.username, '1234',code=1)
        self.assertEqual('失败',self.loginpage.get_loginTips())

if __name__ == "__main__":
    unittest.main()
