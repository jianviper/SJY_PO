#!/usr/bin/env python
#coding:utf-8
import unittest
from common.get_config import get_url, get
from pages.Page_wk_folder import Folder
from parts.tool_worker import *
from parts.tool_page import tiyan

'''
Create on 2020-4-7
author:linjian
summary:文件夹的测试用例
'''


class FolderTest(unittest.TestCase):
    def setUp(self) -> None:
        urls = get_url()  #return [url,home_url]
        self.url, self.home_url = urls[0], urls[1]
        self.username = '14500000050'
        self.password = '123456'
        self.f_PO = Folder(base_url=self.url)
        self.projectName = project_name()
        self.f_title = folder_title()
        self.f_PO.open()

    def tearDown(self) -> None:
        public_tearDown(self.f_PO, self.url, self.home_url, self.username, self.password)
        self.f_PO.driver.quit()

    def add_folder(self, num):
        #添加文件夹
        public_addTool(self.f_PO, self.f_PO.tool_folder_loc, self.f_PO.el_folder_loc, num=num)
        #是否新建成功
        self.assertEqual(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True), num)
        public_revoke_recovery(self.f_PO, self.f_PO.el_folder_loc, step=num)
        self.assertEqual(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True), num)
        '''
        if num > 1:
            selection(self.f_PO, self.f_PO.el_folder_loc)
        rightClick(self.f_PO, el=self.f_PO.el_folder_loc, action=self.f_PO.btn_fdel_loc)
        #是否删除成功
        self.assertFalse(public_check(self.f_PO, self.f_PO.el_folder_loc))
        public_revoke(self.f_PO, self.f_PO.el_folder_loc, type='del', step=num)
        # click_trash(self.f_PO)  #打开废纸篓进行恢复
        recovery(self.f_PO)
        #检查恢复是否成功
        self.assertTrue(public_check(self.f_PO, self.f_PO.el_folder_loc))
        '''

    def test_add_folder(self):
        '''添加文件夹,删除/恢复'''
        public_init(self.f_PO, self.username, self.password, self.projectName)
        self.add_folder(1)

    def test_ty_add_folder(self):
        '''体验模式-添加文件夹,删除/恢复'''
        tiyan(self.f_PO)
        self.add_folder(2)

    def copy(self):
        #复制粘贴，文件夹里添加其它元素
        public_addTool(self.f_PO, self.f_PO.tool_folder_loc, self.f_PO.el_folder_loc)
        self.f_PO.enter()  #双击进入文件夹
        public_check(self.f_PO, self.f_PO.tool_loc)
        ws_add(self.f_PO, [('t', 1), ('i', 1), ('f', 1), ('file', 1)])
        self.assertEqual(public_check(self.f_PO, self.f_PO.el_divs_loc, islen=True), 4)
        el_click(self.f_PO, self.f_PO.btn_bread_loc)
        #复制，粘贴
        rightClick(self.f_PO, el=self.f_PO.el_folder_loc, action=self.f_PO.btn_fcopy_loc)
        rightClick(self.f_PO, 400, 150, self.f_PO.header_loc, self.f_PO.btn_paste_loc)
        self.assertEqual(public_check(self.f_PO, self.f_PO.el_divs_loc, islen=True), 2)
        #进入粘贴后的文件夹
        if len(self.f_PO.find_elements(*self.f_PO.el_folder_loc)) > 1:
            for i in range(len(self.f_PO.find_elements(*self.f_PO.el_folder_loc))):
                self.f_PO.enter(i)
                self.assertEqual(public_check(self.f_PO, self.f_PO.el_divs_loc, islen=True), 4)
                el_click(self.f_PO, self.f_PO.btn_bread_loc)
                self.assertTrue(public_check(self.f_PO, self.f_PO.el_folder_loc))
        sleep(3)

    def test_copy(self):
        '''复制粘贴文件夹'''
        public_init(self.f_PO, self.username, self.password, self.projectName)
        self.copy()

    def tes1t_ty_copy(self):
        '''体验模式-复制粘贴文件夹'''
        tiyan(self.f_PO)
        self.copy()

    def cut(self, num):
        public_addTool(self.f_PO, self.f_PO.tool_folder_loc, self.f_PO.el_folder_loc, num=num)
        self.assertEqual(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True), num)
        poi_src = public_getElPoi(self.f_PO, self.f_PO.el_folder_loc)
        if num > 1:
            selection(self.f_PO, self.f_PO.el_folder_loc)
        rightClick(self.f_PO, el=self.f_PO.el_folder_loc, action=self.f_PO.btn_fjianqie_loc)
        #检查是否剪切成功
        self.assertFalse(public_check(self.f_PO, self.f_PO.el_folder_loc))
        left_click(self.f_PO, 50, -50, el=self.f_PO.tool_loc)
        #剪切成功后左键点击画布，检查是否有出现元素（BUG点）
        self.assertEqual(public_check(self.f_PO, self.f_PO.el_divs_loc, islen=True), 0)
        rightClick(self.f_PO, action=self.f_PO.btn_paste_loc)
        self.assertEqual(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True), num)
        poi_dst = public_getElPoi(self.f_PO, self.f_PO.el_folder_loc)
        public_revoke_recovery(self.f_PO, self.f_PO.el_folder_loc, type='cut', poi_src=poi_src, poi_dst=poi_dst)

    def test_cut(self):
        '''剪切，粘贴'''
        public_init(self.f_PO, self.username, self.password, self.projectName)
        self.cut(1)
        public_delProject(self.f_PO, self.home_url)

    def test_ty_cut(self):
        '''体验模式-剪切，粘贴'''
        tiyan(self.f_PO)
        self.cut(1)

    def test_multiShear(self):
        '''多选剪切，粘贴'''
        public_init(self.f_PO, self.username, self.password, self.projectName)
        self.cut(2)
        public_delProject(self.f_PO, self.home_url)

    def tes1t_ty_multiShear(self):
        '''体验模式-多选剪切，粘贴'''
        tiyan(self.f_PO)
        self.cut(2)

    def multiDel(self):
        public_addTool(self.f_PO, self.f_PO.tool_folder_loc, self.f_PO.el_folder_loc, num=2)
        #检查是否上传成功
        self.assertEqual(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True), 2)
        selection(self.f_PO, self.f_PO.el_folder_loc)
        rightClick(self.f_PO, el=self.f_PO.el_folder_loc, action=self.f_PO.btn_fdel_loc)
        #是否删除成功
        self.assertFalse(public_check(self.f_PO, self.f_PO.el_folder_loc))
        # click_trash(self.f_PO)  #打开废纸篓进行恢复
        # recovery(self.f_PO)
        #检查恢复是否成功
        # self.assertEqual(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True), 2)

    def tes1t_multiDel(self):
        '''多选删除,恢复'''
        public_init(self.f_PO, self.username, self.password, self.projectName)
        self.multiDel()
        public_delProject(self.f_PO, self.home_url)

    def tes1t_ty_multiDel(self):
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

    def tes1t_ty_editTile(self):
        '''体验模式-文件夹标题编辑'''
        tiyan(self.f_PO)
        self.editTitle()

    def test_doubleFolderCopy(self):
        '''多文件夹，多选复制/粘贴，跨项目'''
        public_init(self.f_PO, self.username, self.password, self.projectName)
        public_addTool(self.f_PO, self.f_PO.tool_folder_loc, self.f_PO.el_folder_loc, num=2)
        self.assertEqual(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True), 2)
        selection(self.f_PO, self.f_PO.el_folder_loc)
        #右键-复制
        rightClick(self.f_PO, el=self.f_PO.el_folder_loc, action=self.f_PO.btn_fcopy_loc)
        #右键-粘贴
        rightClick(self.f_PO, 450, 10, self.f_PO.el_folder_loc, self.f_PO.btn_paste_loc)
        #检查个数
        self.assertEqual(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True), 4)
        '''
        self.f_PO.driver.get(self.home_url)
        #进行跨白板粘贴
        public_createProject(self.f_PO, '[copy]' + self.projectName[:13])
        public_intoProject(self.f_PO)
        rightClick(self.f_PO, 150, 10, self.f_PO.tool_loc, self.f_PO.btn_paste_loc)
        self.f_PO.driver.refresh()
        self.assertEqual(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True), 2)

        public_delProject(self.f_PO, self.home_url)
        '''

    def changeColor(self):
        '''改变文件夹颜色'''
        public_addTool(self.f_PO, self.f_PO.tool_folder_loc, self.f_PO.el_folder_loc)
        src = public_getAttrs(self.f_PO, self.f_PO.el_folderImg_loc, 'src')[0]
        rightClick(self.f_PO, el=self.f_PO.el_folder_loc, action=self.f_PO.btn_color_loc)
        green_src = get('folder', 'icon')
        self.assertFalse(public_check(self.f_PO, self.f_PO.right_menu_loc))
        dst = public_getAttrs(self.f_PO, self.f_PO.el_folderImg_loc, 'src')[0]
        print(green_src, '\r\n', dst)
        self.assertTrue(dst == green_src)
        public_revoke_recovery(self.f_PO, self.f_PO.el_folderImg_loc, type='cc', src=src, dst=dst)

    def test_changeColor(self):
        '''改变文件夹颜色'''
        public_init(self.f_PO, self.username, self.password, self.projectName)
        self.changeColor()
        public_delProject(self.f_PO, self.home_url)

    def tes1t_ty_changeColor(self):
        '''体验模式，改变文件夹颜色'''
        tiyan(self.f_PO)
        self.changeColor()

    def test_copyWL(self):
        '''带有关联线的复制，粘贴'''
        public_init(self.f_PO, self.username, self.password, self.projectName)
        addWithLine(self.f_PO, [('f', 1), ('t', 1)], self.f_PO.el_folder_loc, self.f_PO.el_text_loc)
        selection(self.f_PO, [self.f_PO.el_folder_loc, self.f_PO.el_text_loc])
        #复制，粘贴
        rightClick(self.f_PO, el=self.f_PO.el_folder_loc, action=self.f_PO.btn_fcopy_loc)
        rightClick(self.f_PO, 500, 150, self.f_PO.header_loc, self.f_PO.btn_paste_loc)
        self.assertEqual(public_check(self.f_PO, self.f_PO.el_folder_loc, islen=True), 2)
        #self.assertEqual(public_check(self.f_PO, self.f_PO.el_line_loc, islen=True, driver=True), 2)
        self.assertEqual(public_check(self.f_PO, self.f_PO.el_line2_loc, islen=True, driver=True), 2)

        sleep(3)


if __name__ == "__main__":
    # unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(FolderTest('test_ty_add_folder'))
    unittest.TextTestRunner().run(suite)
