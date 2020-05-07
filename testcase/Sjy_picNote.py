#!/usr/bin/env python
#coding:utf-8
import unittest
from time import strftime, localtime
from pages.Page_wk_img import WokerPic
from parts.tool_worker import *

'''
Create on 2020-4-7
author:linjian
summary:图片便签的测试用例(无上传图片功能)
'''


class ImgNoteTest(unittest.TestCase):
    def setUp(self) -> None:
        url = 'https://app.bimuyu.tech/login'
        #url = 'http://test.bimuyu.tech/login'
        self.home_url = 'https://app.bimuyu.tech/home'
        self.username = '14500000050'
        self.password = '123456'
        self.pic_PO = WokerPic(base_url=url)
        self._nowtime = strftime("%Y-%m-%d %H:%M:%S", localtime())
        self.projectName = '自动化测试项目-{0}'.format(self._nowtime)
        self.textContent = '自动化测试文本-{0}'.format(self._nowtime)
        self.pic_PO.open()

    def tearDown(self) -> None:
        self.pic_PO.driver.get(self.home_url)
        if public_check(self.pic_PO, (By.CLASS_NAME, 'item_text'), islen=True) > 2:
            public_delProject(self.pic_PO, self.home_url)
        self.pic_PO.driver.quit()

    def test_del(self):
        '''单张删除/恢复'''
        public_login(self.pic_PO, self.username, self.password)
        public_intoProject(self.pic_PO, el=self.pic_PO.headless_img_loc)
        rightClick_action(self.pic_PO, el=self.pic_PO.el_imgDIV_loc, actionEl=self.pic_PO.btn_del_loc)
        #是否删除成功
        self.assertFalse(public_check(self.pic_PO, self.pic_PO.el_imgDIV_loc))
        click_trash(self.pic_PO)  #打开废纸篓进行恢复
        recovery(self.pic_PO)
        #检查恢复是否成功
        self.assertTrue(public_check(self.pic_PO, self.pic_PO.el_imgDIV_loc, islen=True) == 1)
        sleep(3)

    def test_shear(self):
        '''单张剪切/粘贴'''
        public_login(self.pic_PO, self.username, self.password)
        public_intoProject(self.pic_PO, self.pic_PO.headless_img_loc)
        rightClick_action(self.pic_PO, el=self.pic_PO.el_imgDIV_loc, actionEl=self.pic_PO.btn_jianqie_loc)
        #检查是否剪切成功
        self.assertFalse(public_check(self.pic_PO, self.pic_PO.el_imgDIV_loc))
        left_click(self.pic_PO, 200, 50, el=self.pic_PO.tool_loc)
        #剪切成功后左键点击画布，检查是否有出现元素（BUG点）
        self.assertTrue(public_check(self.pic_PO, self.pic_PO.el_divs_loc, islen=True) == 2)
        rightClick_action(self.pic_PO, actionEl=self.pic_PO.btn_zhantie_loc)
        self.assertTrue(public_check(self.pic_PO, self.pic_PO.el_imgDIV_loc, islen=True) == 1)
        sleep(3)

    def test_multiDel(self):
        '''多选删除/恢复'''
        public_login(self.pic_PO, self.username, self.password)
        public_intoProject(self.pic_PO, self.pic_PO.headless_multiImg_loc)
        if public_check(self.pic_PO, self.pic_PO.el_imgDIV_loc, islen=True) < 2:
            recovery(self.pic_PO)
        selection(self.pic_PO, self.pic_PO.el_imgDIV_loc)
        rightClick_action(self.pic_PO, el=self.pic_PO.el_imgDIV_loc, actionEl=self.pic_PO.btn_del_loc)
        #是否删除成功
        self.assertFalse(public_check(self.pic_PO, self.pic_PO.el_imgDIV_loc))
        click_trash(self.pic_PO)  #打开废纸篓进行恢复
        recovery(self.pic_PO)
        #检查恢复是否成功
        self.assertTrue(public_check(self.pic_PO, self.pic_PO.el_imgDIV_loc, islen=True) == 2)
        sleep(3)

    def test_multiShear(self):
        '''多选剪切，粘贴'''
        public_login(self.pic_PO, self.username, self.password)
        public_intoProject(self.pic_PO, self.pic_PO.headless_multiImg_loc)
        if public_check(self.pic_PO, self.pic_PO.el_imgDIV_loc, islen=True) < 2:
            recovery(self.pic_PO)
        selection(self.pic_PO, self.pic_PO.el_imgDIV_loc)  #多选，下一步进行剪切
        rightClick_action(self.pic_PO, el=self.pic_PO.el_imgDIV_loc, actionEl=self.pic_PO.btn_jianqie_loc)
        #检查是否剪切成功
        self.assertFalse(public_check(self.pic_PO, self.pic_PO.el_imgDIV_loc))
        left_click(self.pic_PO, 200, 50, el=self.pic_PO.tool_loc)
        #剪切成功后左键点击画布，检查是否有出现元素（BUG点）
        self.assertTrue(public_check(self.pic_PO, self.pic_PO.el_divs_loc, islen=True) == 2)
        rightClick_action(self.pic_PO, actionEl=self.pic_PO.btn_zhantie_loc)
        self.assertTrue(public_check(self.pic_PO, self.pic_PO.el_imgDIV_loc, islen=True) == 2)
        sleep(3)


if __name__ == '__main__':
    unittest.main()
