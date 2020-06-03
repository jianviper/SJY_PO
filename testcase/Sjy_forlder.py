#!/usr/bin/env python
#coding:utf-8
import unittest
from common.get_config import get_url
from pages.Page_wk_forlder import WorkerForlder
from parts.tool_worker import *

'''
Create on 2020-4-7
author:linjian
summary:文件夹的测试用例
'''


class Forldertest(unittest.TestCase):
    def setUp(self) -> None:
        urls = get_url()  #return [url,home_url]
        self.url, self.home_url = urls[0], urls[1]
        self.username = '14500000050'
        self.password = '123456'
        self.f_PO = WorkerForlder(base_url=self.url)
        self.projectName = project_name()
        self.f_PO.open()

    def tearDown(self) -> None:
        public_tearDown(self.f_PO, self.url, self.home_url, self.username, self.password)
        self.f_PO.driver.quit()

    def te1st_add_folder(self):
        '''添加文件夹,删除/恢复'''
        public_init(self.f_PO, self.username, self.password, self.projectName)
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

        public_delProject(self.f_PO, self.home_url)

    def te1st_shear(self):
        '''剪切，粘贴'''
        public_init(self.f_PO, self.username, self.password, self.projectName)
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

        public_delProject(self.f_PO, self.home_url)

    def te1st_multiShear(self):
        '''多选剪切，粘贴'''
        public_init(self.f_PO, self.username, self.password, self.projectName)
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

        public_delProject(self.f_PO, self.home_url)

    def te1st_multiDel(self):
        '''多选删除,恢复'''
        public_init(self.f_PO, self.username, self.password, self.projectName)
        public_addTool(self.f_PO, self.f_PO.tool_folder_loc, self.f_PO.el_folder_loc, nums=2)
        #检查是否上传成功
        self.assertTrue(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True) == 2)
        selection(self.f_PO, self.f_PO.el_folder_loc)
        rightClick_action(self.f_PO, el=self.f_PO.el_folder_loc, actionEl=self.f_PO.btn_fdel_loc)
        #是否删除成功
        self.assertFalse(public_check(self.f_PO, self.f_PO.el_folder_loc))
        click_trash(self.f_PO)  #打开废纸篓进行恢复
        recovery(self.f_PO)
        #检查恢复是否成功
        self.assertTrue(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True) == 2)

        public_delProject(self.f_PO, self.home_url)

    def test_editTitle(self):
        '''文件夹标题编辑'''
        public_init(self.f_PO, self.username, self.password, self.projectName)
        public_addTool(self.f_PO, self.f_PO.tool_folder_loc, self.f_PO.el_folder_loc)
        #是否新建成功
        self.assertTrue(public_check(self.f_PO, self.f_PO.el_folder_loc))
        self.f_PO.input_title()  #输入标题文字
        self.f_PO.driver.refresh()
        self.assertTrue(public_check(self.f_PO, self.f_PO.el_folder_loc))

        public_delProject(self.f_PO, self.home_url)

    def te1st_doubleForlderCopy(self):
        '''多文件夹，多选复制/粘贴，跨项目'''
        public_init(self.f_PO, self.username, self.password, self.projectName)
        public_addTool(self.f_PO, self.f_PO.tool_folder_loc, self.f_PO.el_folder_loc, nums=2)
        self.assertIs(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True), 2)
        selection(self.f_PO, self.f_PO.el_folder_loc)
        #右键-复制
        rightClick_action(self.f_PO, el=self.f_PO.el_folder_loc, actionEl=self.f_PO.btn_fcopy_loc)
        #右键-粘贴
        rightClick_action(self.f_PO, 450, 10, self.f_PO.el_folder_loc, self.f_PO.btn_zhantie_loc)
        #检查个数
        self.assertIs(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True), 4)
        sleep(2)
        self.f_PO.driver.get(self.home_url)
        #进行跨白板粘贴
        public_createProject(self.f_PO, '[copy]' + self.projectName)
        public_intoProject(self.f_PO)
        rightClick_action(self.f_PO, 300, 200, self.f_PO.svg_loc, self.f_PO.btn_zhantie_loc)
        self.f_PO.driver.refresh()
        self.assertIs(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True), 2)

        public_delProject(self.f_PO, self.home_url)


if __name__ == "__main__":
    unittest.main()
