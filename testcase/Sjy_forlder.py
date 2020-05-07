#!/usr/bin/env python
#coding:utf-8
import unittest
from time import strftime, localtime
from pages.Page_wk_forlder import WorkerForlder
from parts.tool_worker import *

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
        self.f_PO = WorkerForlder(base_url=url)
        self._nowtime = strftime("%Y-%m-%d %H:%M:%S", localtime())
        self.projectName = '自动化测试项目-{0}'.format(self._nowtime)
        self.textContent = '自动化测试文本-{0}'.format(self._nowtime)
        self.f_PO.open()

    def tearDown(self) -> None:
        self.f_PO.driver.get(self.home_url)
        if public_check(self.f_PO, (By.CLASS_NAME, 'item_text'), islen=True) > 2:
            public_delProject(self.f_PO, self.home_url)
        self.f_PO.driver.quit()

    def test_add_folder(self):
        '''添加文件夹,删除/恢复'''
        public_login(self.f_PO, self.username, self.password)
        public_createProject(self.f_PO, self.projectName)
        public_intoProject(self.f_PO)
        public_addTool(self.f_PO, self.f_PO.tool_folder_loc, self.f_PO.el_folder_loc)
        #是否新建成功
        self.assertTrue(public_check(self.f_PO, self.f_PO.el_folder_loc))
        rightClick_action(self.f_PO, el=self.f_PO.el_folder_loc, actionEl=self.f_PO.btn_fdel_loc)
        #是否删除成功
        self.assertFalse(public_check(self.f_PO, self.f_PO.el_folder_loc))
        click_trash(self.f_PO)  #打开废纸篓进行恢复
        recovery(self.f_PO)
        #检查恢复是否成功
        self.assertTrue(public_check(self.f_PO, self.f_PO.el_folder_loc))
        sleep(3)
        public_delProject(self.f_PO, self.home_url)

    def test_shear(self):
        '''剪切，粘贴'''
        public_login(self.f_PO, self.username, self.password)
        public_createProject(self.f_PO, self.projectName)
        public_intoProject(self.f_PO)
        public_addTool(self.f_PO, self.f_PO.tool_folder_loc, self.f_PO.el_folder_loc)
        #是否新建成功
        self.assertTrue(public_check(self.f_PO, self.f_PO.el_folder_loc))
        rightClick_action(self.f_PO, el=self.f_PO.el_folder_loc, actionEl=self.f_PO.btn_fjianqie_loc)
        #是否剪切成功
        self.assertFalse(public_check(self.f_PO, self.f_PO.el_folder_loc))
        left_click(self.f_PO, 200, 50, self.f_PO.tool_loc)  #点击画布检查
        self.assertTrue(public_check(self.f_PO, self.f_PO.el_divs_loc, islen=True) == 2)
        rightClick_action(self.f_PO, actionEl=self.f_PO.btn_zhantie_loc)
        #是否粘贴成功
        self.assertTrue(public_check(self.f_PO, self.f_PO.el_folder_loc))
        sleep(3)
        public_delProject(self.f_PO, self.home_url)

    def test_multiShear(self):
        '''多选剪切，粘贴'''
        public_login(self.f_PO, self.username, self.password)
        public_createProject(self.f_PO, self.projectName)
        public_intoProject(self.f_PO)
        public_addTool(self.f_PO, self.f_PO.tool_folder_loc, self.f_PO.el_folder_loc, nums=2)
        self.assertTrue(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True) == 2)
        selection(self.f_PO, self.f_PO.el_folder_loc)
        rightClick_action(self.f_PO, el=self.f_PO.el_folder_loc, actionEl=self.f_PO.btn_fjianqie_loc)
        #检查是否剪切成功
        self.assertFalse(public_check(self.f_PO, self.f_PO.el_folder_loc))
        left_click(self.f_PO, 200, 150, el=self.f_PO.svg_loc)
        #剪切成功后左键点击画布，检查是否有出现元素（BUG点）
        self.assertTrue(public_check(self.f_PO, self.f_PO.el_divs_loc, islen=True) == 2)
        rightClick_action(self.f_PO, actionEl=self.f_PO.btn_zhantie_loc)
        self.assertTrue(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True) == 2)
        sleep(3)
        public_delProject(self.f_PO, self.home_url)

    def test_multiDel(self):
        '''多选删除,恢复'''
        public_login(self.f_PO, self.username, self.password)
        public_createProject(self.f_PO, self.projectName)
        public_intoProject(self.f_PO)
        public_addTool(self.f_PO, self.f_PO.tool_folder_loc, self.f_PO.el_folder_loc, nums=2)
        #检查是否上传成功
        self.assertTrue(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True) == 2)
        selection(self.f_PO,self.f_PO.el_folder_loc)
        rightClick_action(self.f_PO, el=self.f_PO.el_folder_loc, actionEl=self.f_PO.btn_fdel_loc)
        #是否删除成功
        self.assertFalse(public_check(self.f_PO, self.f_PO.el_folder_loc))
        click_trash(self.f_PO)  #打开废纸篓进行恢复
        recovery(self.f_PO)
        #检查恢复是否成功
        self.assertTrue(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True) == 2)
        sleep(3)
        public_delProject(self.f_PO, self.home_url)

    def te1st_editTitle(self):
        '''文件夹标题编辑'''
        public_login(self.f_PO, self.username, self.password)
        public_createProject(self.f_PO, self.projectName)
        public_intoProject(self.f_PO)
        public_addTool(self.f_PO, self.f_PO.tool_folder_loc, self.f_PO.el_folder_loc)
        #是否新建成功
        self.assertTrue(public_check(self.f_PO, self.f_PO.el_folder_loc))


if __name__ == "__main__":
    unittest.main()
