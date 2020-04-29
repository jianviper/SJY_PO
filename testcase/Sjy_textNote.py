#!/usr/bin/env python
#coding:utf-8
import unittest
from time import strftime, localtime
from pages.Page_worker import WorkerPage
from parts.pageTools import *

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
        self.textPO = WorkerPage(base_url=url)
        self._nowtime = strftime("%Y-%m-%d %H:%M:%S", localtime())
        self.projectName = '自动化测试项目-{0}'.format(self._nowtime)
        self.textContent = '自动化测试文本-{0}'.format(self._nowtime)
        self.textPO.open()

    def tearDown(self) -> None:
        self.textPO.driver.get(self.home_url)
        if self.textPO.check((By.CLASS_NAME, 'item_text'), islen=True) > 1:
            public_delProject(self.textPO, self.home_url)
        self.textPO.driver.quit()

    def te1st_add_text(self):
        '''添加文本便签,若成功，添加内容'''
        public_login(self.textPO, self.username, self.password)
        public_createProject(self.textPO, self.projectName)
        self.textPO.click_intoProject()
        public_addTool(self.textPO, self.textPO.tool_text_loc, self.textPO.el_textNote_loc)
        #是否新建成功
        self.assertTrue(self.textPO.check(self.textPO.el_textNote_loc))
        self.textPO.input_textNote(self.textContent)  #点击文本便签，再输入文本
        #点击画布
        self.textPO.action_click(150, 100, self.textPO.svg_loc)
        self.assertTrue(self.textPO.check(self.textPO.el_textNoteText_loc, self.textContent))
        self.textPO.driver.refresh()
        #刷新页面数据是否还在
        self.assertTrue(self.textPO.check(self.textPO.el_textNoteText_loc, self.textContent))
        public_delProject(self.textPO, self.home_url)
        sleep(3)

    def test_del_text(self):
        '''删除,恢复文本便签'''
        public_login(self.textPO, self.username, self.password)
        public_createProject(self.textPO, self.projectName)
        self.textPO.click_intoProject()
        public_addTool(self.textPO, self.textPO.tool_text_loc, self.textPO.el_textNote_loc)
        #点击画布
        self.textPO.action_click(150, 100, self.textPO.svg_loc)
        #是否新建成功
        self.assertTrue(self.textPO.check(self.textPO.el_textNote_loc))
        self.textPO.input_textNote(self.textContent)  #点击文本便签，再输入文本
        #检查文本数据
        self.assertTrue(self.textPO.check(self.textPO.el_textNoteText_loc, self.textContent))
        self.textPO.rightClick_action(el=self.textPO.el_textNote_loc, actionEL=self.textPO.btn_del_loc)
        #是否删除成功
        self.assertFalse(self.textPO.check(self.textPO.el_textNote_loc))
        self.textPO.click_trash()
        self.textPO.recovery()
        #是否恢复成功
        self.assertTrue(self.textPO.check(self.textPO.el_textNote_loc))
        #恢复后的数据是否还在
        self.assertTrue(self.textPO.check(self.textPO.el_textNoteText_loc, self.textContent))
        public_delProject(self.textPO, self.home_url)
        sleep(3)

    def te1st_shear(self):
        '''剪切，粘贴'''
        public_login(self.textPO, self.username, self.password)
        public_createProject(self.textPO, self.projectName)
        self.textPO.click_intoProject()
        public_addTool(self.textPO, self.textPO.tool_text_loc, self.textPO.el_textNote_loc)
        #是否新建成功
        self.assertTrue(self.textPO.check(self.textPO.el_textNote_loc))
        self.textPO.input_textNote(self.textContent)  #点击文本便签，再输入文本
        #点击画布
        self.textPO.action_click(150, 100, self.textPO.svg_loc)
        self.assertTrue(self.textPO.check(self.textPO.el_textNoteText_loc, self.textContent))
        self.textPO.rightClick_action(el=self.textPO.el_textNoteText_loc, actionEL=self.textPO.btn_jianqie_loc)
        #检查剪切是否成功
        self.assertFalse(self.textPO.check(self.textPO.el_textNote_loc))
        #剪切后左键点击画布，检查是否会有文件夹多出（BUG点）
        self.textPO.action_click(200, 50, el=self.textPO.tool_loc)
        self.assertTrue(self.textPO.check(self.textPO.el_divs_loc, islen=True) == 2)
        self.textPO.rightClick_action(actionEL=self.textPO.btn_zhantie_loc)
        self.assertTrue(self.textPO.check(self.textPO.el_textNote_loc))
        sleep(3)
        public_delProject(self.textPO, self.home_url)

    def te1st_multiShear(self):
        '''多选剪切，粘贴'''
        public_login(self.textPO, self.username, self.password)
        public_createProject(self.textPO, self.projectName)
        self.textPO.click_intoProject()
        public_addTool(self.textPO, self.textPO.tool_text_loc, self.textPO.el_textNote_loc, nums=2)
        self.assertTrue(self.textPO.check(self.textPO.el_textNote_loc, islen=True) == 2)
        self.textPO.input_textNote(self.textContent)  #点击文本便签，再输入文本
        self.assertTrue(self.textPO.check(self.textPO.el_textNoteText_loc, self.textContent))
        self.textPO.selection(self.textPO.el_textNote_loc) #多选
        self.textPO.rightClick_action(el=self.textPO.el_textNote_loc, actionEL=self.textPO.btn_jianqie_loc)
        #检查是否剪切成功
        self.assertFalse(self.textPO.check(self.textPO.el_textNote_loc))
        self.textPO.action_click(200, 150, el=self.textPO.svg_loc)
        #剪切成功后左键点击画布，检查是否有出现元素（BUG点）
        self.assertTrue(self.textPO.check(self.textPO.el_divs_loc, islen=True) == 2)
        self.textPO.rightClick_action(actionEL=self.textPO.btn_zhantie_loc)
        self.assertTrue(self.textPO.check(self.textPO.el_textNote_loc, islen=True) == 2)
        sleep(3)
    
    def te1st_multiDel(self):
        '''多选删除,恢复'''
        public_login(self.textPO, self.username, self.password)
        public_createProject(self.textPO, self.projectName)
        self.textPO.click_intoProject()
        public_addTool(self.textPO, self.textPO.tool_text_loc, self.textPO.el_textNote_loc,nums=2)
        #是否新建成功
        self.assertTrue(self.textPO.check(self.textPO.el_textNote_loc))
        self.textPO.input_textNote(self.textContent)  #点击文本便签，再输入文本
        self.assertTrue(self.textPO.check(self.textPO.el_textNoteText_loc, self.textContent))
        self.textPO.selection(self.textPO.el_textNote_loc) #多选
        self.textPO.rightClick_action(el=self.textPO.el_textNote_loc,actionEL=self.textPO.btn_del_loc)
        #是否删除成功
        self.assertFalse(self.textPO.check(self.textPO.el_textNote_loc))
        self.textPO.click_trash()  #打开废纸篓进行恢复
        self.textPO.recovery()
        #检查恢复是否成功
        self.assertTrue(self.textPO.check(self.textPO.el_textNote_loc, islen=True) == 2)
        sleep(3)
        public_delProject(self.textPO, self.home_url)


if __name__ == "__main__":
    unittest.main()
