#!/usr/bin/env python
#coding:utf-8
import unittest
from time import strftime, localtime
from pages.Page_worker import WorkerPage
from parts.pageTools import *

'''
Create on 2020-4-7
author:linjian
summary:文件夹的测试用例
'''


class ForlderTest(unittest.TestCase):
    def setUp(self) -> None:
        url = 'https://app.bimuyu.tech/login'
        #url = 'http://test.bimuyu.tech/login'
        self.home_url = 'http://app.bimuyu.tech/home'
        self.username = '14500000050'
        self.password = '123456'
        self.forlderPO = WorkerPage(base_url=url)
        self._nowtime = strftime("%Y-%m-%d %H:%M:%S", localtime())
        self.projectName = '自动化测试项目-{0}'.format(self._nowtime)
        self.textContent = '自动化测试文本-{0}'.format(self._nowtime)
        self.forlderPO.open()

    def tearDown(self) -> None:
        self.forlderPO.driver.get(self.home_url)
        if self.forlderPO.check((By.CLASS_NAME, 'item_text'), islen=True) > 2:
            public_delProject(self.forlderPO, self.home_url)
        self.forlderPO.driver.quit()

    def test_add_folder(self):
        '''添加文件夹'''
        public_login(self.forlderPO, self.username, self.password)
        public_createProject(self.forlderPO, self.projectName)
        self.forlderPO.click_intoProject()
        public_addTool(self.forlderPO, self.forlderPO.tool_folder_loc, self.forlderPO.el_folder_loc)
        #是否新建成功
        self.assertTrue(self.forlderPO.check(self.forlderPO.el_folder_loc))
        self.forlderPO.rightClick_action(el=self.forlderPO.el_folder_loc, actionEL=self.forlderPO.btn_fdel_loc)
        #是否删除成功
        self.assertFalse(self.forlderPO.check(self.forlderPO.el_folder_loc))
        sleep(3)
        public_delProject(self.forlderPO, self.home_url)

    def test_shear(self):
        '''剪切，粘贴'''
        public_login(self.forlderPO, self.username, self.password)
        public_createProject(self.forlderPO, self.projectName)
        self.forlderPO.click_intoProject()
        public_addTool(self.forlderPO, self.forlderPO.tool_folder_loc, self.forlderPO.el_folder_loc)
        #是否新建成功
        self.assertTrue(self.forlderPO.check(self.forlderPO.el_folder_loc))
        self.forlderPO.rightClick_action(el=self.forlderPO.el_folder_loc, actionEL=self.forlderPO.btn_fjianqie_loc)
        #是否剪切成功
        self.assertFalse(self.forlderPO.check(self.forlderPO.el_folder_loc))
        self.forlderPO.action_click(200, 50, self.forlderPO.tool_loc)  #点击画布检查
        self.assertTrue(self.forlderPO.check(self.forlderPO.el_divs_loc, islen=True) == 2)
        self.forlderPO.rightClick_action(actionEL=self.forlderPO.btn_zhantie_loc)
        #是否粘贴成功
        self.assertTrue(self.forlderPO.check(self.forlderPO.el_folder_loc))
        sleep(3)
        public_delProject(self.forlderPO, self.home_url)

    def test_multiShear(self):
        '''多选剪切，粘贴'''
        public_login(self.forlderPO, self.username, self.password)
        public_createProject(self.forlderPO, self.projectName)
        self.forlderPO.click_intoProject()
        public_addTool(self.forlderPO, self.forlderPO.tool_folder_loc, self.forlderPO.el_folder_loc, nums=2)
        self.assertTrue(self.forlderPO.check(self.forlderPO.el_folder_loc, islen=True) == 2)
        self.forlderPO.selection(self.forlderPO.el_folder_loc)
        self.forlderPO.rightClick_action(el=self.forlderPO.el_folder_loc, actionEL=self.forlderPO.btn_fjianqie_loc)
        #检查是否剪切成功
        self.assertFalse(self.forlderPO.check(self.forlderPO.el_folder_loc))
        self.forlderPO.action_click(200, 150, el=self.forlderPO.svg_loc)
        #剪切成功后左键点击画布，检查是否有出现元素（BUG点）
        self.assertTrue(self.forlderPO.check(self.forlderPO.el_divs_loc, islen=True) == 2)
        self.forlderPO.rightClick_action(actionEL=self.forlderPO.btn_zhantie_loc)
        self.assertTrue(self.forlderPO.check(self.forlderPO.el_folder_loc, islen=True) == 2)
        sleep(3)

    def test_multiDel(self):
        '''多选删除,恢复'''
        public_login(self.forlderPO, self.username, self.password)
        public_createProject(self.forlderPO, self.projectName)
        self.forlderPO.click_intoProject()
        public_addTool(self.forlderPO, self.forlderPO.tool_folder_loc, self.forlderPO.el_folder_loc, nums=2)
        #检查是否上传成功
        self.assertTrue(self.forlderPO.check(self.forlderPO.el_folder_loc, islen=True) == 2)
        self.forlderPO.selection(self.forlderPO.el_folder_loc)
        self.forlderPO.rightClick_action(el=self.forlderPO.el_folder_loc, actionEL=self.forlderPO.btn_fdel_loc)
        #是否删除成功
        self.assertFalse(self.forlderPO.check(self.forlderPO.el_folder_loc))
        self.forlderPO.click_trash()  #打开废纸篓进行恢复
        self.forlderPO.recovery()
        #检查恢复是否成功
        self.assertTrue(self.forlderPO.check(self.forlderPO.el_folder_loc, islen=True) == 2)
        sleep(3)
        public_delProject(self.forlderPO, self.home_url)


if __name__ == "__main__":
    unittest.main()
