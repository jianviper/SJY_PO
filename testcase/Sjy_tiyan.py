#!/usr/bin/env python
#coding:utf-8
import unittest
from common.get_config import get_url
from pages.Page_invite import InvitePage
from parts.tool_worker import *

'''
Create on 2020-6-3
author:linjian
summary:体验用户的测试用例
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
        '''体验'''


if __name__ == "__main__":
    unittest.main()
