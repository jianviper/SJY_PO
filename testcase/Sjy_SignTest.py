#!/usr/bin/env python
import unittest
from common.get_config import get_url
from pages.Page_login import LoginPage
from parts.tool_page import public_check

'''
Create on 2020-3-17
author:linjian
summary:使用unittest框架编写测试用例
'''


class LoginTest(unittest.TestCase):
    def setUp(self):
        urls = get_url()  #return [url,home_url]
        self.url = urls[0]
        self.username = '14500000050'
        self.username_format_error = '145000'
        self.password = '123456'
        self.password_error = '999999'
        self.password_format_error = '123'
        self.login_PO = LoginPage(base_url=self.url)

    def tearDown(self):
        self.login_PO.driver.quit()

    #用例执行体
    def test_sign(self):
        '''正确的账号密码登录'''
        #声明signpage对象
        #执行具体操作
        self.login_PO.login(self.username, self.password, flag=1)
        self.assertEqual('登录成功', self.login_PO.get_loginTips())
        self.assertEqual('比幕鱼 - 白板列表', self.login_PO.driver.title)

    def test_phone_format_error(self):
        '''使用格式错误的手机号登录'''
        self.login_PO.login(self.username_format_error, self.password)
        self.assertEqual('🙃请填写正确的手机号', self.login_PO.get_warnTitle())

    def test_password_error(self):
        '''使用错误的密码登录'''
        self.login_PO.login(self.username, self.password_error)
        self.assertEqual('账号或密码错误', self.login_PO.get_loginTips())

    def test_password_format_error(self):
        '''使用格式错误的密码登录'''
        self.login_PO.login(self.username, self.password_format_error)
        self.assertEqual("🙃密码不符合要求", self.login_PO.get_warnTitle())

    def test_CodeLogin_noCode(self):
        '''未填写验证码的情况下进行登录'''
        self.login_PO.login(self.username, '', code=1)
        self.assertTrue(public_check(self.login_PO, self.login_PO.warnTitle_loc))

    def test_CodeLogin_errorCode(self):
        '''使用错误的验证码的进行登录'''
        self.login_PO.login(self.username, 0000, code=1)
        self.assertEqual('短信验证失败', self.login_PO.get_loginTips())


if __name__ == "__main__":
    unittest.main()
