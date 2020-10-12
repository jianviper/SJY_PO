#!/usr/bin/env python
#coding:utf-8
import unittest, warnings
from common.get_config import get_url
from pages.Page_worker import WorkerPage
from parts.tool_worker import *

'''
Create on 2020-7-30
author:linjian
summary:撤销/恢复的测试用例
'''


class RevokeTest(unittest.TestCase):
    def setUp(self) -> None:
        warnings.simplefilter('ignore', ResourceWarning)
        urls = get_url()  #return [url,home_url]
        self.url, self.home_url = urls[0], urls[1]
        self.username = '14500000050'
        self.username2 = '14500000051'
        self.password = '123456'
        self.revoke_PO = WorkerPage(base_url=self.url)
        self.projectName = project_name()
        self.textContent = textNote_Content()
        self.revoke_PO.open()

    def tearDown(self) -> None:
        public_tearDown(self.revoke_PO, self.url, self.home_url, self.username, self.password)
        self.revoke_PO.driver.quit()

    def createNote(self, tool=None, el=None):
        #新建元素，设置对应元素的复制和剪切
        cut = self.revoke_PO.menu_cut_loc
        copy = self.revoke_PO.menu_copy_loc
        if tool == 'img':
            public_add(self.revoke_PO, [('i', 1)])
            cut = self.revoke_PO.menu_imgCut_loc
            copy = self.revoke_PO.menu_imgCopy_loc
        else:
            public_addTool(self.revoke_PO, tool, el)
            left_click(self.revoke_PO, 50, 100, self.revoke_PO.header_loc)
        if tool == self.revoke_PO.tool_folder_loc:
            cut = self.revoke_PO.menu_fcut_loc
            copy = self.revoke_PO.menu_fcopy_loc
        return {"copy": copy, "cut": cut}

    def creatAndInput(self, tool=None, el=None, **kwargs):
        #新建便签，撤销-恢复，若是文本便签，再输入内容，撤销-恢复
        # public_addTool(self.revoke_PO, self.revoke_PO.tool_text_loc, self.revoke_PO.el_textNote_loc)
        self.createNote(tool, el)
        left_click(self.revoke_PO, 50, 100, self.revoke_PO.header_loc)
        do_revoke(self.revoke_PO)  #撤销
        #检查撤销是否成功，成功则文本便签不存在
        self.assertFalse(public_check(self.revoke_PO, el))
        do_recovery(self.revoke_PO)  #恢复
        #检查恢复是否成功，成功则文本便签存在
        self.assertTrue(public_check(self.revoke_PO, el))
        if kwargs.get('type') == 'text':
            public_textInput(self.revoke_PO, self.textContent)
            do_revoke(self.revoke_PO)  #撤销
            self.assertTrue(self.revoke_PO.get_textContent() == '')
            do_recovery(self.revoke_PO)  #恢复
            self.assertTrue(self.revoke_PO.get_textContent() != '')
        sleep(3)

    def test_textNote(self):
        '''文本便签的新建，输入的撤销与恢复'''
        public_init(self.revoke_PO, self.username, self.password, self.projectName)
        self.creatAndInput(self.revoke_PO.tool_text_loc, self.revoke_PO.el_textNote_loc, type='text')

    def test_ty_textNote(self):
        '''体验模式下，文本便签的新建，输入的撤销与恢复'''
        tiyan(self.revoke_PO)
        self.creatAndInput(self.revoke_PO.tool_text_loc, self.revoke_PO.el_textNote_loc, type='text')

    def test_imgNote(self):
        '''图片便签新建的撤销与恢复'''
        public_init(self.revoke_PO, self.username, self.password, self.projectName)
        self.creatAndInput('img', self.revoke_PO.el_imgNote_loc)

    def test_ty_imgNote(self):
        '''体验模式下，图片便签的新建，撤销与恢复'''
        tiyan(self.revoke_PO)
        self.creatAndInput('img', self.revoke_PO.el_imgNote_loc)

    def test_folder(self):
        '''文件夹新建后，撤销与恢复'''
        public_init(self.revoke_PO, self.username, self.password, self.projectName)
        self.creatAndInput(self.revoke_PO.tool_folder_loc, self.revoke_PO.el_folder_loc)

    def test_ty_folder(self):
        tiyan(self.revoke_PO)
        self.creatAndInput(self.revoke_PO.tool_folder_loc, self.revoke_PO.el_folder_loc)

    def cutAndPaste(self, tool=None, el=None):
        '''便签的剪切粘贴的撤销和恢复'''
        cut = self.createNote(tool, el)
        #获取元素初始位置
        poi_src = public_getElPosition(self.revoke_PO, el)[0]
        rightClick(self.revoke_PO, el=el, action=cut)
        #检查剪切是否成功
        self.assertFalse(public_check(self.revoke_PO, el))
        #剪切后左键点击画布，检查是否会有文件夹多出（BUG点）
        left_click(self.revoke_PO, 50, 100, el=self.revoke_PO.header_loc)
        self.assertIs(public_check(self.revoke_PO, self.revoke_PO.el_divs_loc, islen=True), 0)
        #在指定位置粘贴-------------------
        rightClick(self.revoke_PO, 700, 200, self.revoke_PO.header_loc,
                   action=self.revoke_PO.menu_paste_loc)
        self.assertTrue(public_check(self.revoke_PO, el))
        #获取元素剪切粘贴后的位置
        poi_dst = public_getElPosition(self.revoke_PO, el)[0]
        print('{0}\r\n{1}'.format(poi_src, poi_dst))
        do_revoke(self.revoke_PO)  #执行撤销
        poi_src2 = public_getElPosition(self.revoke_PO, el)[0]
        self.assertTrue(poi_src == poi_src2)  #如果撤销正常，和初始位置一样
        do_recovery(self.revoke_PO)  #执行恢复
        poi_dst2 = public_getElPosition(self.revoke_PO, el)[0]
        self.assertTrue(poi_dst == poi_dst2)  #如果恢复正常，和粘贴后位置一样

    def test_textNoteCut(self):
        public_init(self.revoke_PO, self.username, self.password, self.projectName)
        self.cutAndPaste(self.revoke_PO.tool_text_loc, self.revoke_PO.el_textNote_loc)

    def test_imgNote(self):
        public_init(self.revoke_PO, self.username, self.password, self.projectName)
        self.cutAndPaste('img', self.revoke_PO.el_imgNote_loc)

    def test_folder(self):
        public_init(self.revoke_PO, self.username, self.password, self.projectName)
        self.cutAndPaste(self.revoke_PO.tool_folder_loc, self.revoke_PO.el_folder_loc)


if __name__ == "__main__":
    unittest.main()
