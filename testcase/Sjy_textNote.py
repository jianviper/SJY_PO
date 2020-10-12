#!/usr/bin/env python
#coding:utf-8
import unittest
from common.get_config import get_url
from pages.Page_wk_textNote import WorkerTextNote
from parts.tool_worker import *
from parts.tool_page import tiyan

from factory.elementFactory import ElementCreater

'''
Create on 2020-4-7
author:linjian
summary:文本便签的测试用例
'''


class textNoteTest(unittest.TestCase):
    def setUp(self) -> None:
        urls = get_url()  #return [url,home_url]
        self.url, self.home_url = urls[0], urls[1]
        self.username = '14500000050'
        self.password = '123456'
        self.text_PO = WorkerTextNote(base_url=self.url)
        self.projectName = project_name()
        self.textContent = textNote_Content()
        self.textNote = ElementCreater().create_element('text', self.text_PO)
        self.text_PO.open()

    def tearDown(self) -> None:
        public_tearDown(self.text_PO, self.url, self.home_url, self.username, self.password)
        self.text_PO.driver.quit()

    def addAndDel(self, num):
        #添加文本便签,若成功，添加内容
        public_addTool(self.text_PO, self.text_PO.tool_text_loc, self.text_PO.el_textNote_loc, num=num)
        #是否新建成功
        self.assertIs(public_check(self.text_PO, self.text_PO.el_textNote_loc, islen=True), num)
        sleep(3)
        public_revoke(self.text_PO, self.text_PO.el_textNote_loc, step=num)  #撤销，恢复
        public_textInput(self.text_PO, self.textContent)  #点击文本便签，再输入文本
        #点击画布
        left_click(self.text_PO, 100, 80, self.text_PO.header_loc)
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNoteText_loc, self.textContent))
        public_revoke(self.text_PO, type='input', step=num)
        # self.text_PO.driver.refresh()
        #刷新页面数据是否还在
        # self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNoteText_loc, self.textContent))
        if num > 1:
            selection(self.text_PO, self.text_PO.el_textNote_loc)  #多选
        rightClick(self.text_PO, el=self.text_PO.el_textNote_loc, action=self.text_PO.btn_del_loc)
        #是否删除成功
        self.assertFalse(public_check(self.text_PO, self.text_PO.el_textNote_loc))
        public_revoke(self.text_PO, self.text_PO.el_textNote_loc, type='del', step=num)
        # click_trash(self.text_PO)  #打开废纸篓进行恢复
        # recovery(self.text_PO)
        #是否恢复成功
        # self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNote_loc))
        #恢复后的数据是否还在
        # self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNoteText_loc, self.textContent))

    def test_addAndDel(self):
        '''添加文本便签,若成功，添加内容,然后删除再恢复'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
        self.addAndDel(1)

    def test_ty_addAndDel(self):
        '''体验模式-添加文本便签,若成功，添加内容,然后删除再恢复'''
        tiyan(self.text_PO)
        self.addAndDel(1)

    def test_multiaddAndDel(self):
        '''多选删除,恢复'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
        self.addAndDel(2)

    def test_ty_muladdAndDel(self):
        '''体验模式-多选删除,恢复'''
        tiyan(self.text_PO)
        self.addAndDel(2)

    def cut(self, num):
        #剪切，粘贴
        public_addTool(self.text_PO, self.text_PO.tool_text_loc, self.text_PO.el_textNote_loc, num=num)
        self.assertIs(public_check(self.text_PO, self.text_PO.el_textNote_loc, islen=True), num)
        public_textInput(self.text_PO, self.textContent)  #点击文本便签，再输入文本
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNoteText_loc, self.textContent))
        poi_src = public_getElPosition(self.text_PO, self.text_PO.el_textNote_loc)
        if num > 1:
            selection(self.text_PO, self.text_PO.el_textNote_loc)  #多选
        rightClick(self.text_PO, el=self.text_PO.el_textNote_loc, action=self.text_PO.btn_jianqie_loc)
        #检查是否剪切成功
        self.assertFalse(public_check(self.text_PO, self.text_PO.el_textNote_loc))
        left_click(self.text_PO, 500, 200, self.text_PO.header_loc)
        #剪切成功后左键点击画布，检查是否有出现元素（BUG点）
        self.assertIs(public_check(self.text_PO, self.text_PO.el_divs_loc, islen=True), 0)
        rightClick(self.text_PO, action=self.text_PO.btn_zhantie_loc)
        self.assertIs(public_check(self.text_PO, self.text_PO.el_textNote_loc, islen=True), num)
        poi_dst = public_getElPosition(self.text_PO, self.text_PO.el_textNote_loc)
        public_revoke(self.text_PO, self.text_PO.el_textNote_loc, type='cut', poi_src=poi_src, poi_dst=poi_dst)

    def test_cut(self):
        '''剪切，粘贴'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
        self.cut(1)
        public_delProject(self.text_PO, self.home_url)

    def test_ty_cut(self):
        '''体验模式-剪切，粘贴'''
        tiyan(self.text_PO)
        self.cut(1)

    def test_multicut(self):
        '''多选剪切，粘贴'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
        self.cut(2)
        public_delProject(self.text_PO, self.home_url)

    def test_ty_multicut(self):
        '''体验模式-多选剪切，粘贴'''
        tiyan(self.text_PO)
        self.cut(2)

    def tes1t_drag(self):
        '''拖动到文件夹内'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
        public_addTool(self.text_PO, self.text_PO.tool_text_loc, self.text_PO.el_textNote_loc)
        #是否新建成功
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNote_loc))
        public_textInput(self.text_PO, self.textContent)  #点击文本便签，再输入文本
        #添加文件夹
        public_addTool(self.text_PO, self.text_PO.tool_folder_loc, self.text_PO.el_folder_loc, x=300, y=500)
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_folder_loc))
        #拖动文本便签到文件夹内
        elDrag(self.text_PO, self.text_PO.el_textNote_loc, self.text_PO.el_folder_loc)
        # self.assertFalse(public_check(self.text_PO,self.text_PO.el_textNote_loc))

        public_delProject(self.text_PO, self.home_url)

    def copy(self, num):
        '''复制/粘贴，跨项目'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
        public_addTool(self.text_PO, self.text_PO.tool_text_loc, self.text_PO.el_textNote_loc, num=num)
        #是否新建成功
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNote_loc))
        public_textInput(self.text_PO, self.textContent)  #点击文本便签，再输入文本
        if num > 1:
            selection(self.text_PO, self.text_PO.el_textNote_loc)
        #右键-复制
        rightClick(self.text_PO, el=self.text_PO.el_textNote_loc, action=self.text_PO.btn_copy_loc)
        #右键-粘贴
        rightClick(self.text_PO, 450, 10, self.text_PO.el_textNote_loc, self.text_PO.btn_zhantie_loc)
        self.assertIs(public_check(self.text_PO, self.text_PO.el_textNote_loc, islen=True), num * 2)
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNoteText_loc, self.textContent))
        public_revoke(self.text_PO, self.text_PO.el_textNote_loc, type='copy', num=num)
        sleep(2)
        self.text_PO.driver.get(self.home_url)
        public_createProject(self.text_PO, '[copy]' + self.projectName[6:].replace(' ', ''))
        public_intoProject(self.text_PO)
        rightClick(self.text_PO, 500, 10, self.text_PO.tool_loc, self.text_PO.btn_zhantie_loc)
        self.assertIs(public_check(self.text_PO, self.text_PO.el_textNote_loc, islen=True), num)
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNoteText_loc, self.textContent))
        public_revoke(self.text_PO, self.text_PO.el_textNote_loc)

        public_delProject(self.text_PO, self.home_url)

    def test_copy(self):
        self.copy(1)

    def test_multiCopy(self):
        self.copy(2)

    def test_setBgColor(self):
        #设置文本便签背景色,判断颜色设置是否正确
        public_init(self.text_PO, self.username, self.password, self.projectName)
        public_addTool(self.text_PO, self.text_PO.tool_text_loc, self.text_PO.el_textNote_loc, num=1)
        public_textInput(self.text_PO, self.textContent)
        for i in range(1, 9):
            rightClick(self.text_PO, el=self.text_PO.el_textNote_loc)  #右键点击
            self.text_PO.getc(i, self.textContent)
            sleep(1)

    def test_factory(self):
        public_init(self.text_PO, self.username, self.password, self.projectName)
        self.textNote.add()
        self.textNote.public_textInput(self.textContent)

        sleep(3)


if __name__ == "__main__":
    unittest.main()
