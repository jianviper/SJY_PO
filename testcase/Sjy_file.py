#!/usr/bin/env python
#coding:utf-8
import unittest
from common.get_config import get_url
from pages.Page_wk_file import FilePage
from parts.tool_worker import *

'''
Create on 2020-8-25
author:linjian
summary:文件上传/预览的测试用例
'''


class FileTest(unittest.TestCase):
    def setUp(self) -> None:
        urls = get_url()  #return [url,home_url]
        self.url, self.home_url = urls[0], urls[1]
        self.username = '14500000050'
        self.password = '123456'
        self.file_PO = FilePage(base_url=self.url)
        self.projectName = project_name()
        self.file_PO.open()

    def tearDown(self) -> None:
        public_tearDown(self.file_PO, self.url, self.home_url, self.username, self.password)
        self.file_PO.driver.quit()

    def add(self, num):
        '''
        添加文件
        :param num:文件数量
        :return:
        '''
        ws_add(self.file_PO, [('file', num)])
        self.assertTrue(public_check(self.file_PO, self.file_PO.el_fileview_loc))
        size = public_getElSize(self.file_PO, self.file_PO.el_file_loc)
        for s in size:
            self.assertTrue(int(s['height']), 987)
            self.assertTrue(int(s['width']), 700)

    def test_add(self):
        public_init(self.file_PO, self.username, self.password, self.projectName)
        self.add(2)
        self.assertEqual(public_check(self.file_PO, self.file_PO.el_file_loc, islen=True), 2)
        file_title = get_text(self.file_PO, self.file_PO.el_fileTitle_loc)
        self.assertEqual(file_title, 'websocket.docx')

    def test_fileTool(self):
        public_init(self.file_PO, self.username, self.password, self.projectName)
        self.add(1)
        el_click(self.file_PO, self.file_PO.el_fileview_loc)
        self.assertTrue(public_check(self.file_PO, self.file_PO.el_fileTool_loc))
        el_click(self.file_PO, self.file_PO.btn_nextPage_loc)
        self.assertEqual('2', get_text(self.file_PO, self.file_PO.pageCode_loc))

    def test_ty_fileTool(self):
        tiyan(self.file_PO)
        self.add(1)
        el_click(self.file_PO, self.file_PO.el_fileview_loc)
        self.assertTrue(public_check(self.file_PO, self.file_PO.el_fileTool_loc))
        el_click(self.file_PO, self.file_PO.btn_nextPage_loc)
        self.assertEqual('2', get_text(self.file_PO, self.file_PO.pageCode_loc))

    def copy(self, num):
        '''
        复制/粘贴
        :param num:文件数量
        :return:
        '''
        self.add(num)
        if num > 1:
            selection(self.file_PO, self.file_PO.el_file_loc)
        rightClick(self.file_PO, el=self.file_PO.el_file_loc, action=self.file_PO.menu_copy_loc)
        left_click(self.file_PO, 80, 100, el=self.file_PO.header_loc)
        rightClick(self.file_PO, x=1000, y=100, el=self.file_PO.header_loc, action=self.file_PO.menu_paste_loc)
        self.assertEqual(public_check(self.file_PO, self.file_PO.el_file_loc, islen=True), num * 2)

    def test_copy(self):
        '''单个复制'''
        public_init(self.file_PO, self.username, self.password, self.projectName)
        self.copy(1)

    def tes1t_multiCopy(self):
        '''多选复制'''
        self.copy(2)

    def cut(self, num):
        '''
        剪切/粘贴
        :param num:文件数量
        :return:
        '''
        self.add(num)
        if num > 1:
            selection(self.file_PO, self.file_PO.el_file_loc)
        rightClick(self.file_PO, el=self.file_PO.el_file_loc, action=self.file_PO.menu_cut_loc)
        left_click(self.file_PO, 50, -50, el=self.file_PO.tool_loc)
        #剪切成功后左键点击画布，检查是否有出现元素（BUG点）
        self.assertEqual(public_check(self.file_PO, self.file_PO.el_divs_loc, islen=True), 0)
        rightClick(self.file_PO, x=400, y=150, action=self.file_PO.menu_paste_loc)
        self.assertEqual(public_check(self.file_PO, self.file_PO.el_divs_loc, islen=True), num)

    def test_cut(self):
        '''单个剪切'''
        public_init(self.file_PO, self.username, self.password, self.projectName)
        self.cut(1)

    def tes1t_multiCut(self):
        '''多选剪切'''
        self.cut(2)

    def copyWithLine(self):
        self.add(2)
        el_click(self.file_PO, self.file_PO.el_file_loc)

    def tes1t_pullRelAddEl(self):
        '''拉出关联线，添加元素'''
        self.add(1)
        el_click(self.file_PO, self.file_PO.el_file_loc)
        #拉出关联线
        elDrag(self.file_PO, self.file_PO.btn_relright_loc, 100, 0)
        el_click(self.file_PO, self.file_PO.menu_forlder_loc)  #添加文件夹
        left_click(self.file_PO, 100, 100, self.file_PO.header_loc)
        el_click(self.file_PO, self.file_PO.el_file_loc)
        #拉出关联线
        elDrag(self.file_PO, self.file_PO.btn_relbtm_loc, 0, 100)
        el_click(self.file_PO, self.file_PO.menu_text_loc)  #添加文本
        left_click(self.file_PO, 100, 100, self.file_PO.header_loc)
        self.assertEqual(public_check(self.file_PO, self.file_PO.el_line_loc, islen=True), 2)


if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestSuite()
    # suite.addTest(FileTest('test_ty_fileTool'))
    # unittest.TextTestRunner().run(suite)
