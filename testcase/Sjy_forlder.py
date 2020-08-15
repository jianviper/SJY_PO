#!/usr/bin/env python
#coding:utf-8
import unittest
from common.get_config import get_url, get
from pages.Page_wk_forlder import WorkerForlder
from parts.tool_worker import *
from parts.tool_page import tiyan

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
        self.f_title = forlder_title()
        self.f_PO.open()

    def tearDown(self) -> None:
        public_tearDown(self.f_PO, self.url, self.home_url, self.username, self.password)
        self.f_PO.driver.quit()

    def add_folder(self):
        #添加文件夹
        public_addTool(self.f_PO, self.f_PO.tool_folder_loc, self.f_PO.el_folder_loc)
        #是否新建成功
        self.assertTrue(public_check(self.f_PO, self.f_PO.el_folder_loc))
        public_revoke(self.f_PO, self.f_PO.el_folder_loc)
        rightClick_action(self.f_PO, el=self.f_PO.el_folder_loc, actionEl=self.f_PO.btn_fdel_loc)
        #是否删除成功
        self.assertFalse(public_check(self.f_PO, self.f_PO.el_folder_loc))
        public_revoke(self.f_PO, self.f_PO.el_folder_loc, type='del')
        # click_trash(self.f_PO)  #打开废纸篓进行恢复
        # recovery(self.f_PO)
        #检查恢复是否成功
        # self.assertTrue(public_check(self.f_PO, self.f_PO.el_folder_loc))

    def test_add_folder(self):
        '''添加文件夹,删除/恢复'''
        public_init(self.f_PO, self.username, self.password, self.projectName)
        self.add_folder()

    def test_ty_add_folder(self):
        '''体验模式-添加文件夹,删除/恢复'''
        tiyan(self.f_PO)
        self.add_folder()

    def shear(self, num):
        public_addTool(self.f_PO, self.f_PO.tool_folder_loc, self.f_PO.el_folder_loc, num=num)
        self.assertIs(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True), num)
        poi_src = public_getElPosition(self.f_PO, self.f_PO.el_folder_loc)
        if num > 1:
            selection(self.f_PO, self.f_PO.el_folder_loc)
        rightClick_action(self.f_PO, el=self.f_PO.el_folder_loc, actionEl=self.f_PO.btn_fjianqie_loc)
        #检查是否剪切成功
        self.assertFalse(public_check(self.f_PO, self.f_PO.el_folder_loc))
        left_click(self.f_PO, 50, -50, el=self.f_PO.tool_loc)
        #剪切成功后左键点击画布，检查是否有出现元素（BUG点）
        self.assertIs(public_check(self.f_PO, self.f_PO.el_divs_loc, islen=True), 0)
        rightClick_action(self.f_PO, actionEl=self.f_PO.btn_zhantie_loc)
        self.assertIs(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True), num)
        poi_dst = public_getElPosition(self.f_PO, self.f_PO.el_folder_loc)
        public_revoke(self.f_PO, self.f_PO.el_folder_loc, type='cut', poi_src=poi_src, poi_dst=poi_dst)

    def test_shear(self):
        '''剪切，粘贴'''
        public_init(self.f_PO, self.username, self.password, self.projectName)
        self.shear(1)
        public_delProject(self.f_PO, self.home_url)

    def test_ty_shear(self):
        '''体验模式-剪切，粘贴'''
        tiyan(self.f_PO)
        self.shear(1)

    def test_multiShear(self):
        '''多选剪切，粘贴'''
        public_init(self.f_PO, self.username, self.password, self.projectName)
        self.shear(2)
        public_delProject(self.f_PO, self.home_url)

    def test_ty_multiShear(self):
        '''体验模式-多选剪切，粘贴'''
        tiyan(self.f_PO)
        self.shear(2)

    def multiDel(self):
        public_addTool(self.f_PO, self.f_PO.tool_folder_loc, self.f_PO.el_folder_loc, num=2)
        #检查是否上传成功
        self.assertIs(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True), 2)
        selection(self.f_PO, self.f_PO.el_folder_loc)
        rightClick_action(self.f_PO, el=self.f_PO.el_folder_loc, actionEl=self.f_PO.btn_fdel_loc)
        #是否删除成功
        self.assertFalse(public_check(self.f_PO, self.f_PO.el_folder_loc))
        # click_trash(self.f_PO)  #打开废纸篓进行恢复
        # recovery(self.f_PO)
        #检查恢复是否成功
        # self.assertIs(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True), 2)

    def test_multiDel(self):
        '''多选删除,恢复'''
        public_init(self.f_PO, self.username, self.password, self.projectName)
        self.multiDel()
        public_delProject(self.f_PO, self.home_url)

    def test_ty_multiDel(self):
        '''体验模式-多选删除,恢复'''
        tiyan(self.f_PO)
        self.multiDel()

    def editTitle(self):
        public_addTool(self.f_PO, self.f_PO.tool_folder_loc, self.f_PO.el_folder_loc)
        #是否新建成功
        self.assertTrue(public_check(self.f_PO, self.f_PO.el_folder_loc))
        self.f_PO.input_title(self.f_title)  #输入标题文字
        self.assertTrue(self.f_PO.get_title() == '标题{0}'.format(self.f_title))

    def test_editTitle(self):
        '''文件夹标题编辑'''
        public_init(self.f_PO, self.username, self.password, self.projectName)
        self.editTitle()
        public_delProject(self.f_PO, self.home_url)

    def test_ty_editTile(self):
        '''体验模式-文件夹标题编辑'''
        tiyan(self.f_PO)
        self.editTitle()

    def test_doubleForlderCopy(self):
        '''多文件夹，多选复制/粘贴，跨项目'''
        public_init(self.f_PO, self.username, self.password, self.projectName)
        public_addTool(self.f_PO, self.f_PO.tool_folder_loc, self.f_PO.el_folder_loc, num=2)
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
        rightClick_action(self.f_PO, 150, 10, self.f_PO.tool_loc, self.f_PO.btn_zhantie_loc)
        self.f_PO.driver.refresh()
        self.assertIs(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True), 2)

        public_delProject(self.f_PO, self.home_url)

    def changeColor(self):
        public_addTool(self.f_PO, self.f_PO.tool_folder_loc, self.f_PO.el_folder_loc)
        src = public_getAttrs(self.f_PO, self.f_PO.el_folderImg_loc, 'src')[0]
        rightClick_action(self.f_PO, el=self.f_PO.el_folder_loc, actionEl=self.f_PO.btn_color_loc)
        green_src = get('folder', 'icon')
        self.assertFalse(public_check(self.f_PO, self.f_PO.right_menu_loc))
        dst = public_getAttrs(self.f_PO, self.f_PO.el_folderImg_loc, 'src')[0]
        self.assertTrue(dst == green_src)
        public_revoke(self.f_PO, self.f_PO.el_folderImg_loc, type='cc', src=src, dst=dst)

    def test_changeColor(self):
        public_init(self.f_PO, self.username, self.password, self.projectName)
        self.changeColor()
        public_delProject(self.f_PO, self.home_url)

    def test_ty_changeColor(self):
        tiyan(self.f_PO)
        self.changeColor()


if __name__ == "__main__":
    unittest.main()
