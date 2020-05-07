#!/usr/bin/env python
#coding:utf-8
import unittest
from time import strftime, localtime
from pages.Page_invite import InvitePage
from parts.tool_page import *

'''
Create on 2020-4-7
author:linjian
summary:邀请/加入的测试用例
'''


class InviteTest(unittest.TestCase):
    def setUp(self) -> None:
        url = 'https://app.bimuyu.tech/login'
        #url = 'http://test.bimuyu.tech/login'
        # url = 'http://pre.bimuyu.tech/'
        self.home_url = 'http://app.bimuyu.tech/home'
        # self.home_url = 'http://pre.bimuyu.tech/home'
        self.username = '14500000050'
        self.username2 = '14500000051'
        self.password = '123456'
        self.invitePO = InvitePage(base_url=url)
        self._nowtime = strftime("%Y-%m-%d %H:%M:%S", localtime())
        self.projectName = '自动化测试项目-{0}'.format(self._nowtime)
        self.textContent = '自动化测试文本-{0}'.format(self._nowtime)
        self.invitePO.open()

    def tearDown(self) -> None:
        public_login(self.invitePO, self.username, self.password)
        self.invitePO.driver.get(self.home_url)
        if public_check(self.invitePO, (By.CLASS_NAME, 'item_text'), islen=True) > 2:
            public_delProject(self.invitePO, self.home_url)
        self.invitePO.driver.quit()

    def test_invite(self):
        #邀请/加入/退出
        public_login(self.invitePO, self.username, self.password)
        public_createProject(self.invitePO, self.projectName)
        public_intoProject(self.invitePO)
        self.invitePO.click_invite()
        inviUrl = self.invitePO.get_inviUrl()  #获取邀请链接
        print(inviUrl)
        public_logout(self.invitePO)
        self.invitePO.driver.get(inviUrl)  #打开邀请页面
        sleep(3)
        print('get inviName:', self.invitePO.get_inviName())
        #检查邀请项目的名称是否一致
        self.assertTrue(public_check(self.invitePO, self.invitePO.inviName_loc, text=self.projectName))
        self.invitePO.click_joinInvi()  #点击加入邀请
        public_login(self.invitePO, self.username2, self.password) #登录另一账号
        #检查加入邀请是否成功
        self.assertTrue(public_check(self.invitePO, self.invitePO.lastProjectName_loc, text=self.projectName))
        public_intoProject(self.invitePO)  #进入最后一个项目
        self.invitePO.exit_project()  #退出画布
        self.invitePO.driver.get(self.home_url)
        #检查退出是否成功
        self.assertFalse(public_check(self.invitePO, self.invitePO.lastProjectName_loc, text=self.projectName))
        public_logout(self.invitePO)


if __name__ == "__main__":
    unittest.main()
