#!/usr/bin/env python
#coding:utf-8
import unittest
from time import strftime, localtime
from pages.Page_wk_textNote import WorkerTextNote
from parts.tool_worker import *

'''
Create on 2020-4-7
author:linjian
summary:文本便签的测试用例
'''


class textNoteTest(unittest.TestCase):
    def setUp(self) -> None:
        url = 'https://app.bimuyu.tech/login'
        #url = 'http://test.bimuyu.tech/login'
        self.home_url = 'http://app.bimuyu.tech/home'
        self.username = '14500000050'
        self.password = '123456'
        self.text_PO = WorkerTextNote(base_url=url)
        self._nowtime = strftime("%Y-%m-%d %H:%M:%S", localtime())
        self.projectName = '自动化测试项目-{0}'.format(self._nowtime)
        self.textContent = '自动化测试文本-{0}'.format(self._nowtime)
        self.text_PO.open()

    def tearDown(self) -> None:
        self.text_PO.driver.get(self.home_url)
        if public_check(self.text_PO, (By.CLASS_NAME, 'item_text'), islen=True) > 2:
            public_delProject(self.text_PO, self.home_url)
        self.text_PO.driver.quit()

    def test_add_text(self):
        '''添加文本便签,若成功，添加内容'''
        public_login(self.text_PO, self.username, self.password)
        public_createProject(self.text_PO, self.projectName)
        public_intoProject(self.text_PO)
        public_addTool(self.text_PO, self.text_PO.tool_text_loc, self.text_PO.el_textNote_loc)
        #是否新建成功
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNote_loc))
        self.text_PO.input_textNote(self.textContent)  #点击文本便签，再输入文本
        #点击画布
        left_click(self.text_PO, 150, 100, self.text_PO.svg_loc)
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNoteText_loc, self.textContent))
        self.text_PO.driver.refresh()
        #刷新页面数据是否还在
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNoteText_loc, self.textContent))
        sleep(3)
        public_delProject(self.text_PO, self.home_url)

    def test_del_text(self):
        '''删除,恢复文本便签'''
        public_login(self.text_PO, self.username, self.password)
        public_createProject(self.text_PO, self.projectName)
        public_intoProject(self.text_PO)
        public_addTool(self.text_PO, self.text_PO.tool_text_loc, self.text_PO.el_textNote_loc)
        #点击画布
        left_click(self.text_PO, 150, 100, self.text_PO.svg_loc)
        #是否新建成功
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNote_loc))
        self.text_PO.input_textNote(self.textContent)  #点击文本便签，再输入文本
        #检查文本数据
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNoteText_loc, self.textContent))
        rightClick_action(self.text_PO, el=self.text_PO.el_textNote_loc, actionEl=self.text_PO.btn_del_loc)
        #是否删除成功
        self.assertFalse(public_check(self.text_PO, self.text_PO.el_textNote_loc))
        click_trash(self.text_PO)  #打开废纸篓进行恢复
        recovery(self.text_PO)
        #是否恢复成功
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNote_loc))
        #恢复后的数据是否还在
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNoteText_loc, self.textContent))
        sleep(3)
        public_delProject(self.text_PO, self.home_url)

    def test_shear(self):
        '''剪切，粘贴'''
        public_login(self.text_PO, self.username, self.password)
        public_createProject(self.text_PO, self.projectName)
        public_intoProject(self.text_PO)
        public_addTool(self.text_PO, self.text_PO.tool_text_loc, self.text_PO.el_textNote_loc)
        #是否新建成功
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNote_loc))
        self.text_PO.input_textNote(self.textContent)  #点击文本便签，再输入文本
        #点击画布
        left_click(self.text_PO, 150, 100, self.text_PO.svg_loc)
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNoteText_loc, self.textContent))
        rightClick_action(self.text_PO, el=self.text_PO.el_textNoteText_loc, actionEl=self.text_PO.btn_jianqie_loc)
        #检查剪切是否成功
        self.assertFalse(public_check(self.text_PO, self.text_PO.el_textNote_loc))
        #剪切后左键点击画布，检查是否会有文件夹多出（BUG点）
        left_click(self.text_PO, 200, 50, el=self.text_PO.tool_loc)
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_divs_loc, islen=True) == 2)
        rightClick_action(self.text_PO, actionEl=self.text_PO.btn_zhantie_loc)
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNote_loc))
        sleep(3)
        public_delProject(self.text_PO, self.home_url)

    def test_multiShear(self):
        '''多选剪切，粘贴'''
        public_login(self.text_PO, self.username, self.password)
        public_createProject(self.text_PO, self.projectName)
        public_intoProject(self.text_PO)
        public_addTool(self.text_PO, self.text_PO.tool_text_loc, self.text_PO.el_textNote_loc, nums=2)
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNote_loc, islen=True) == 2)
        self.text_PO.input_textNote(self.textContent)  #点击文本便签，再输入文本
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNoteText_loc, self.textContent))
        selection(self.text_PO, self.text_PO.el_textNote_loc)  #多选
        rightClick_action(self.text_PO, el=self.text_PO.el_textNote_loc, actionEl=self.text_PO.btn_jianqie_loc)
        #检查是否剪切成功
        self.assertFalse(public_check(self.text_PO, self.text_PO.el_textNote_loc))
        left_click(self.text_PO, 200, 150, el=self.text_PO.svg_loc)
        #剪切成功后左键点击画布，检查是否有出现元素（BUG点）
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_divs_loc, islen=True) == 2)
        rightClick_action(self.text_PO, actionEl=self.text_PO.btn_zhantie_loc)
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNote_loc, islen=True) == 2)
        sleep(3)
        public_delProject(self.text_PO, self.home_url)

    def test_multiDel(self):
        '''多选删除,恢复'''
        public_login(self.text_PO, self.username, self.password)
        public_createProject(self.text_PO, self.projectName)
        public_intoProject(self.text_PO)
        public_addTool(self.text_PO, self.text_PO.tool_text_loc, self.text_PO.el_textNote_loc, nums=2)
        #是否新建成功
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNote_loc))
        self.text_PO.input_textNote(self.textContent)  #点击文本便签，再输入文本
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNoteText_loc, self.textContent))
        selection(self.text_PO, self.text_PO.el_textNote_loc)  #多选
        rightClick_action(self.text_PO, el=self.text_PO.el_textNote_loc, actionEl=self.text_PO.btn_del_loc)
        #是否删除成功
        self.assertFalse(public_check(self.text_PO, self.text_PO.el_textNote_loc))
        click_trash(self.text_PO)  #打开废纸篓进行恢复
        recovery(self.text_PO)
        #检查恢复是否成功
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNote_loc, islen=True) == 2)
        sleep(3)
        public_delProject(self.text_PO, self.home_url)


if __name__ == "__main__":
    unittest.main()
