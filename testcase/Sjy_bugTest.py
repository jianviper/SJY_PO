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


class BugTest(unittest.TestCase):

    def setUp(self) -> None:
        urls = get_url()  #return [url,home_url]
        self.url, self.home_url = urls[0], urls[1]
        self.username = '14500000050'
        self.username2 = '14500000051'
        self.password = '123456'
        self.bug_PO = WorkerPage(base_url=self.url)
        self.projectName = project_name()
        self.textContent = textNote_Content()
        self.bug_PO.open()

    def tearDown(self) -> None:
        public_tearDown(self.bug_PO, self.url, self.home_url, self.username, self.password)
        self.bug_PO.driver.quit()

    def cutCopy(self):
        #添加图片便签
        # public_addTool(self.bug_PO, self.bug_PO.tool_img_loc, self.bug_PO.el_imgDIV_loc)
        public_add(self.bug_PO, [('i', 1)])
        self.assertTrue(public_check(self.bug_PO, self.bug_PO.el_img_loc, attr='src'))
        #添加文本便签
        public_addTool(self.bug_PO, self.bug_PO.tool_text_loc, self.bug_PO.tool_text_loc, x=200, y=400)
        public_textInput(self.bug_PO, self.textContent)  #点击文本便签，再输入文本
        #先剪切图片再复制文本便签，再点击画布
        rightClick(self.bug_PO, el=self.bug_PO.el_imgDIV_loc, actionEl=self.bug_PO.btn_imgCut_loc)
        rightClick(self.bug_PO, el=self.bug_PO.el_textNote_loc, actionEl=self.bug_PO.btn_copy_loc)
        left_click(self.bug_PO, 100, -100, self.bug_PO.tool_mouse_loc)
        #检查是否有文件夹产生
        self.assertFalse(public_check(self.bug_PO, self.bug_PO.el_folder_loc))

    def test_cutCopy(self):
        '''先右键剪切一个图片便签，再右键复制一个文本便签，再左键点击画布空白处
        https://www.teambition.com/task/5eb90afe593a4a001a00128e'''
        public_init(self.bug_PO, self.username, self.password, self.projectName)
        self.cutCopy()

    def test_ty_cutCopy(self):
        '''体验模式-先右键剪切一个图片便签，再右键复制一个文本便签，再左键点击画布空白处'''
        tiyan(self.bug_PO)
        self.cutCopy()


if __name__ == "__main__":
    unittest.main()
