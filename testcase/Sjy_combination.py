#!/usr/bin/env python
#coding:utf-8
import unittest
from common.get_config import get_url
from pages.Page_worker import WorkerPage
from parts.tool_worker import *
from parts.tool_page import tiyan

'''
Create on 2020-4-7
author:linjian
summary:邀请/加入的测试用例
'''


class CombinationTest(unittest.TestCase):

    def setUp(self) -> None:
        urls = get_url()  #return [url,home_url]
        self.url, self.home_url = urls[0], urls[1]
        self.username = '14500000050'
        self.username2 = '14500000051'
        self.password = '123456'
        self.comb_PO = WorkerPage(base_url=self.url)
        self.projectName = project_name()
        self.textContent = textNote_Content()
        self.comb_PO.open()

    def tearDown(self) -> None:
        public_tearDown(self.comb_PO, self.url, self.home_url, self.username, self.password)
        self.comb_PO.driver.quit()

    def textAndimg(self):
        public_add(self.comb_PO, [('t', 1), ('i', 1)])
        #是否新建成功
        self.assertTrue(public_check(self.comb_PO, self.comb_PO.el_img_loc, attr='src'))
        self.assertTrue(public_check(self.comb_PO, self.comb_PO.el_textNote_loc))
        #框选，右键剪切，粘贴
        selection(self.comb_PO, [self.comb_PO.el_textNote_loc, self.comb_PO.el_imgDIV_loc])
        rightClick_action(self.comb_PO, el=self.comb_PO.el_imgDIV_loc, actionEl=self.comb_PO.btn_imgCut_loc)
        left_click(self.comb_PO, 50, 100, self.comb_PO.header_loc)
        self.assertIs(public_check(self.comb_PO, self.comb_PO.el_divs_loc, islen=True), 0)
        rightClick_action(self.comb_PO, 400, 150, self.comb_PO.header_loc, actionEl=self.comb_PO.btn_paste_loc)
        #检查是否粘贴成功
        self.assertTrue(public_check(self.comb_PO, self.comb_PO.el_img_loc, attr='src'))
        self.assertTrue(public_check(self.comb_PO, self.comb_PO.el_textNote_loc))

        #框选，右键复制，粘贴
        selection(self.comb_PO, [self.comb_PO.el_textNote_loc, self.comb_PO.el_imgDIV_loc])
        rightClick_action(self.comb_PO, el=self.comb_PO.el_imgDIV_loc, actionEl=self.comb_PO.btn_imgCopy_loc)
        left_click(self.comb_PO, 50, -80, self.comb_PO.tool_mouse_loc)
        self.assertIs(public_check(self.comb_PO, self.comb_PO.el_divs_loc, islen=True), 2)
        rightClick_action(self.comb_PO, 200, 400, self.comb_PO.tool_loc, actionEl=self.comb_PO.btn_paste_loc)
        #检查是否粘贴成功
        self.assertIs(len(public_check(self.comb_PO, self.comb_PO.el_img_loc, attr='src')), 2)
        self.assertIs(public_check(self.comb_PO, self.comb_PO.el_textNote_loc, islen=True), 2)

    def test_textAndimg(self):
        '''文本便签和图片便签的组合剪切粘贴，复制粘贴的操作'''
        public_init(self.comb_PO, self.username, self.password, self.projectName)
        self.textAndimg()
        public_delProject(self.comb_PO, self.home_url)

    def test_ty_textAndimg(self):
        '''体验模式-文本便签和图片便签的组合剪切粘贴，复制粘贴的操作'''
        tiyan(self.comb_PO)
        self.textAndimg()

    def textAndfolder(self):
        public_add(self.comb_PO, [('t', 1), ('f', 1)])
        #是否新建成功
        self.assertTrue(public_check(self.comb_PO, self.comb_PO.el_folder_loc))
        self.assertTrue(public_check(self.comb_PO, self.comb_PO.el_textNote_loc))
        #框选，右键剪切，粘贴
        selection(self.comb_PO, [self.comb_PO.el_textNote_loc, self.comb_PO.el_folder_loc])
        rightClick_action(self.comb_PO, el=self.comb_PO.el_folder_loc, actionEl=self.comb_PO.btn_fcut_loc)
        left_click(self.comb_PO, 50, -80, self.comb_PO.tool_mouse_loc)
        self.assertIs(public_check(self.comb_PO, self.comb_PO.el_divs_loc, islen=True), 0)
        rightClick_action(self.comb_PO, 200, 10, self.comb_PO.tool_loc, actionEl=self.comb_PO.btn_paste_loc)
        #检查是否粘贴成功
        self.assertTrue(public_check(self.comb_PO, self.comb_PO.el_folder_loc))
        self.assertTrue(public_check(self.comb_PO, self.comb_PO.el_textNote_loc))
        #框选，右键复制，粘贴
        selection(self.comb_PO, [self.comb_PO.el_textNote_loc, self.comb_PO.el_folder_loc])
        rightClick_action(self.comb_PO, el=self.comb_PO.el_folder_loc, actionEl=self.comb_PO.btn_fcopy_loc)
        left_click(self.comb_PO, 50, -80, self.comb_PO.tool_mouse_loc)
        self.assertIs(public_check(self.comb_PO, self.comb_PO.el_divs_loc, islen=True), 2)
        rightClick_action(self.comb_PO, 200, 400, self.comb_PO.tool_loc, actionEl=self.comb_PO.btn_paste_loc)
        #检查是否粘贴成功
        self.assertIs(public_check(self.comb_PO, self.comb_PO.el_folder_loc, islen=True), 2)
        self.assertIs(public_check(self.comb_PO, self.comb_PO.el_textNote_loc, islen=True), 2)

    def test_textAndfolder(self):
        '''文本便签和文件夹的组合剪切粘贴，复制粘贴的操作'''
        public_init(self.comb_PO, self.username, self.password, self.projectName)
        self.textAndfolder()
        public_delProject(self.comb_PO, self.home_url)

    def test_ty_textAndfolder(self):
        '''体验模式-文本便签和文件夹的组合剪切粘贴，复制粘贴的操作'''
        tiyan(self.comb_PO)
        self.textAndfolder()

    def imgAndfolder(self):
        public_add(self.comb_PO, [('i', 1), ('f', 1)])
        #是否新建成功
        self.assertTrue(public_check(self.comb_PO, self.comb_PO.el_img_loc, attr='src'))
        self.assertTrue(public_check(self.comb_PO, self.comb_PO.el_folder_loc))
        #框选，右键剪切，粘贴
        selection(self.comb_PO, [self.comb_PO.el_folder_loc, self.comb_PO.el_imgDIV_loc])
        rightClick_action(self.comb_PO, el=self.comb_PO.el_imgDIV_loc, actionEl=self.comb_PO.btn_imgCut_loc)
        left_click(self.comb_PO, 50, -80, self.comb_PO.tool_mouse_loc)
        self.assertIs(public_check(self.comb_PO, self.comb_PO.el_divs_loc, islen=True), 0)
        rightClick_action(self.comb_PO, 200, 10, self.comb_PO.tool_loc, actionEl=self.comb_PO.btn_paste_loc)
        #检查是否粘贴成功
        self.assertTrue(public_check(self.comb_PO, self.comb_PO.el_img_loc, attr='src'))
        self.assertTrue(public_check(self.comb_PO, self.comb_PO.el_folder_loc))
        #框选，右键复制，粘贴
        selection(self.comb_PO, [self.comb_PO.el_folder_loc, self.comb_PO.el_imgDIV_loc])
        rightClick_action(self.comb_PO, el=self.comb_PO.el_imgDIV_loc, actionEl=self.comb_PO.btn_imgCopy_loc)
        left_click(self.comb_PO, 50, -80, self.comb_PO.tool_mouse_loc)
        self.assertIs(public_check(self.comb_PO, self.comb_PO.el_divs_loc, islen=True), 2)
        rightClick_action(self.comb_PO, 600, -20, self.comb_PO.tool_loc, actionEl=self.comb_PO.btn_paste_loc)
        #检查是否粘贴成功
        self.assertIs(len(public_check(self.comb_PO, self.comb_PO.el_img_loc, attr='src')), 2)
        self.assertIs(public_check(self.comb_PO, self.comb_PO.el_folder_loc, islen=True), 2)

    def test_imgAndfolder(self):
        '''图片便签和文件夹的组合剪切粘贴，复制粘贴的操作'''
        public_init(self.comb_PO, self.username, self.password, self.projectName)
        self.imgAndfolder()
        public_delProject(self.comb_PO, self.home_url)

    def test_ty_imgAndfolder(self):
        '''体验模式-图片便签和文件夹的组合剪切粘贴，复制粘贴的操作'''
        tiyan(self.comb_PO)
        self.imgAndfolder()

    def textAndimg2(self):
        public_add(self.comb_PO, [('t', 1), ('i', 1)])
        #是否新建成功
        self.assertTrue(public_check(self.comb_PO, self.comb_PO.el_img_loc, attr='src'))
        self.assertTrue(public_check(self.comb_PO, self.comb_PO.el_textNote_loc))
        #框选，右键剪切，粘贴
        selection(self.comb_PO, [self.comb_PO.el_textNote_loc, self.comb_PO.el_imgDIV_loc])
        rightClick_action(self.comb_PO, el=self.comb_PO.el_imgDIV_loc, actionEl=self.comb_PO.btn_imgCut_loc)
        left_click(self.comb_PO, 50, -50, self.comb_PO.tool_loc)
        self.assertIs(public_check(self.comb_PO, self.comb_PO.el_divs_loc, islen=True), 0)
        rightClick_action(self.comb_PO, 200, 10, self.comb_PO.tool_loc, actionEl=self.comb_PO.btn_paste_loc)
        #检查是否粘贴成功
        self.assertTrue(public_check(self.comb_PO, self.comb_PO.el_img_loc, attr='src'))
        self.assertTrue(public_check(self.comb_PO, self.comb_PO.el_textNote_loc))
        #框选，右键复制，粘贴
        selection(self.comb_PO, [self.comb_PO.el_textNote_loc, self.comb_PO.el_imgDIV_loc])
        rightClick_action(self.comb_PO, el=self.comb_PO.el_imgDIV_loc, actionEl=self.comb_PO.btn_imgCopy_loc)
        left_click(self.comb_PO, 50, -50, self.comb_PO.tool_loc)
        self.assertIs(public_check(self.comb_PO, self.comb_PO.el_divs_loc, islen=True), 2)
        rightClick_action(self.comb_PO, 200, 400, self.comb_PO.tool_loc, actionEl=self.comb_PO.btn_paste_loc)
        #检查是否粘贴成功
        self.assertIs(len(public_check(self.comb_PO, self.comb_PO.el_img_loc, attr='src')), 2)
        self.assertIs(public_check(self.comb_PO, self.comb_PO.el_textNote_loc, islen=True), 2)

    def test_textAndimg2(self):
        '''文本便签和图片便签的组合,挨个剪切，再粘贴，挨个复制再粘贴的操作'''
        public_init(self.comb_PO, self.username, self.password, self.projectName)
        self.textAndimg2()
        public_delProject(self.comb_PO, self.home_url)

    def test_ty_textAndimg2(self):
        '''体验模式-文本便签和图片便签的组合,挨个剪切，再粘贴，挨个复制再粘贴的操作'''
        tiyan(self.comb_PO)
        self.textAndimg2()


if __name__ == "__main__":
    unittest.main()
