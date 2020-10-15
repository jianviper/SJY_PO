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
        public_init(self.file_PO, self.username, self.password, self.projectName)
        public_add(self.file_PO, [('file', num)])
        self.assertTrue(public_check(self.file_PO, self.file_PO.el_file_loc))

    def copy(self, num):
        '''
        复制/粘贴
        :param num:文件数量
        :return:
        '''
        self.add(num)
        rightClick(self.file_PO, el=self.file_PO.el_file_loc, action=self.file_PO.menu_copy_loc)
        left_click(self.file_PO, 80, 100, el=self.file_PO.header_loc)
        rightClick(self.file_PO, x=400, y=150, action=self.file_PO.menu_paste_loc)
        self.assertIs(public_check(self.file_PO, self.file_PO.el_file_loc, islen=True), num * 2)
        selection(self.file_PO, self.file_PO.el_file_loc)
        rightClick(self.file_PO, el=self.file_PO.el_file_loc, action=self.file_PO.menu_copy_loc)
        left_click(self.file_PO, 50, -50, el=self.file_PO.tool_loc)
        rightClick(self.file_PO, x=200, y=400, action=self.file_PO.menu_paste_loc)
        self.assertIs(public_check(self.file_PO, self.file_PO.el_file_loc, islen=True), num * 4)

    def test_copy(self):
        '''单个复制'''
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
        self.assertIs(public_check(self.file_PO, self.file_PO.el_divs_loc, islen=True), 0)
        rightClick(self.file_PO, x=400, y=150, action=self.file_PO.menu_paste_loc)
        self.assertIs(public_check(self.file_PO, self.file_PO.el_divs_loc, islen=True), num)

    def test_cut(self):
        '''单个剪切'''
        self.cut(1)

    def test_multiCut(self):
        '''多选剪切'''
        self.cut(2)

    def copyWithLine(self):
        self.add(2)
        self.file_PO.el_click(self.file_PO.el_file_loc)

    def test_pullRelAddEl(self):
        '''拉出关联线，添加元素'''
        self.add(1)
        self.file_PO.el_click(self.file_PO.el_file_loc)
        #拉出关联线
        elDrag(self.file_PO, self.file_PO.btn_relright_loc, 100, 0)
        self.file_PO.el_click(self.file_PO.menu_forlder_loc)  #添加文件夹
        left_click(self.file_PO, 100, 100, self.file_PO.header_loc)
        self.file_PO.el_click(self.file_PO.el_file_loc)
        #拉出关联线
        elDrag(self.file_PO, self.file_PO.btn_relbtm_loc, 0, 100)
        self.file_PO.el_click(self.file_PO.menu_text_loc)  #添加文本便签
        left_click(self.file_PO, 100, 100, self.file_PO.header_loc)
        self.assertIs(public_check(self.file_PO, self.file_PO.el_line_loc, islen=True), 2)

    def test_prePage(self):
        '''预览文件,置顶，关闭'''
        public_init(self.file_PO, self.username, self.password, self.projectName)
        public_add(self.file_PO, [('file', 1), ('f', 1)])
        #右键-预览
        # rightClick(self.file_PO, el=self.file_PO.el_file_loc, action=self.file_PO.menu_pre_loc)
        double_click(self.file_PO, self.file_PO.el_file_loc)  #双击打开
        # tips = self.file_PO.get_text(self.file_PO.tips_loc)  #获取失败提示
        # self.assertTrue(public_check(self.file_PO, self.file_PO.el_prePage_loc), msg=tips)
        self.assertTrue(public_check(self.file_PO, self.file_PO.arrow_loc))
        sleep(2)
        el_click(self.file_PO, self.file_PO.el_preTop_loc)
        double_click(self.file_PO, self.file_PO.el_forlder_loc)
        self.assertTrue(public_check(self.file_PO, self.file_PO.tool_loc))
        self.assertTrue(public_check(self.file_PO, self.file_PO.arrow_loc))
        sleep(2)
        self.file_PO.el_click(self.file_PO.btn_fileclose_loc)  #关闭预览
        self.file_PO.driver.refresh()
        self.assertFalse(public_check(self.file_PO, self.file_PO.el_prePage_loc))


if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(FileTest('test_prePage'))
    unittest.TextTestRunner().run(suite)
