#!/usr/bin/env python
#coding:utf-8
import unittest
from common.get_config import get_url
from pages.Page_invite import InvitePage
from parts.tool_worker import *

'''
Create on 2020-4-7
author:linjian
summary:邀请/加入的测试用例
'''


class InviteTest(unittest.TestCase):
    def setUp(self) -> None:
        urls = get_url()  #return [url,home_url]
        self.url, self.home_url = urls[0], urls[1]
        self.username = '14500000050'
        self.username2 = '14500000051'
        self.password = '123456'
        self.invite_PO = InvitePage(base_url=self.url)
        self.projectName = project_name()
        self.textContent = textNote_Content()
        self.invite_PO.open()

    def tearDown(self) -> None:
        public_tearDown(self.invite_PO, self.url, self.home_url, self.username, self.password)
        self.invite_PO.driver.quit()

    def test_invite(self):
        #邀请/加入/退出
        public_init(self.invite_PO, self.username, self.password, self.projectName)
        public_addTool(self.invite_PO, self.invite_PO.tool_text_loc, self.invite_PO.el_textNote_loc)
        self.invite_PO.click_invite()
        inviUrl = self.invite_PO.get_inviUrl()  #获取邀请链接
        print(inviUrl)
        public_logout(self.invite_PO)  #退出登录
        self.invite_PO.driver.get(inviUrl)  #打开邀请页面
        sleep(2)
        print('get inviName:', self.invite_PO.get_inviName())
        #检查邀请项目的名称是否一致
        self.assertTrue(public_check(self.invite_PO, self.invite_PO.inviName_loc, text=self.projectName))
        self.invite_PO.click_joinInvi()  #点击加入邀请
        public_login(self.invite_PO, self.username2, self.password)  #登录另一账号
        #检查加入邀请是否成功
        self.assertTrue(public_check(self.invite_PO, self.invite_PO.lastProjectName_loc, text=self.projectName))
        public_intoProject(self.invite_PO)  #进入刚加入的项目
        self.assertEqual('比幕鱼 - {0}'.format(self.projectName), self.invite_PO.driver.title)
        self.assertTrue(public_check(self.invite_PO, self.invite_PO.el_textNote_loc))
        self.invite_PO.exit_project()  #退出画布
        self.invite_PO.driver.get(self.home_url)
        #检查退出是否成功
        self.assertFalse(public_check(self.invite_PO, self.invite_PO.lastProjectName_loc, text=self.projectName))
        public_logout(self.invite_PO)


if __name__ == "__main__":
    unittest.main()
