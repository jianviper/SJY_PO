#!/usr/bin/env python
#coding:utf-8
import unittest
from common.get_config import get_url
from pages.Page_share import SharePage
from parts.tool_worker import *

'''
Create on 2020-8-19
author:linjian
summary:分享的测试用例
'''


class ShareTest(unittest.TestCase):
    def setUp(self) -> None:
        urls = get_url()  #return [url,home_url]
        self.url, self.home_url = urls[0], urls[1]
        self.username = '14500000050'
        self.password = '123456'
        self.share_PO = SharePage(base_url=self.url)
        self.projectName = project_name()
        self.share_PO.open()

    def tearDown(self) -> None:
        public_tearDown(self.share_PO, self.url, self.home_url, self.username, self.password)
        self.share_PO.driver.quit()

    def share(self, status):
        '''
        分享
        :param status:0不用登录，1先登录
        :return:
        '''
        public_init(self.share_PO, self.username, self.password, self.projectName)
        public_add(self.share_PO, [('t', 1), ('i', 1), ('f', 1)])
        title = self.share_PO.driver.title
        self.share_PO.click(self.share_PO.btn_userout_loc)
        shareUrl = self.share_PO.get_value(self.share_PO.el_shareUrl_loc)
        public_logout(self.share_PO)
        public_check(self.share_PO, self.share_PO.code_image_loc)
        tip = '当前只能浏览，登录后可保存并编辑该内容'
        if status:  #如果要登录先
            tip = '当前只能浏览，保存后可编辑该内容'
            public_login(self.share_PO, '14500000001', self.password)
        self.share_PO.driver.get(shareUrl)
        self.assertFalse(public_check(self.share_PO, self.share_PO.tool_loc))
        print(title, self.share_PO.driver.title)
        self.assertTrue(self.share_PO.driver.title == title)
        self.assertTrue(self.share_PO.get_text(self.share_PO.el_save_text_loc) == tip)
        self.share_PO.click_save()  #点击"保存"
        if status:
            wait_tips(self.share_PO)
            self.share_PO.driver.get(self.home_url)
        else:
            self.assertTrue(public_check(self.share_PO, self.share_PO.code_image_loc))
            public_login(self.share_PO, '14500000001', self.password)
        self.assertTrue(public_check(self.share_PO, self.share_PO.last_proTitle_loc, text=self.projectName))
        public_delProject(self.share_PO)
        public_logout(self.share_PO)
        public_login(self.share_PO, self.username, self.password)

    def test_unloginShare(self):
        #未登录，打开分享页
        self.share(0)

        sleep(3)

    def test_loggedShare(self):
        #先登录，再打开分享页
        self.share(1)


if __name__ == '__main__':
    unittest.main()
