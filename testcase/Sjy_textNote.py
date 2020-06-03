#!/usr/bin/env python
#coding:utf-8
import unittest
from common.get_config import get_url
from pages.Page_wk_textNote import WorkerTextNote
from parts.tool_worker import *

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
        self.text_PO.open()

    def tearDown(self) -> None:
        public_tearDown(self.text_PO, self.url, self.home_url, self.username, self.password)
        self.text_PO.driver.quit()

    def test_add_text(self):
        '''添加文本便签,若成功，添加内容,然后删除再恢复'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
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
        rightClick_action(self.text_PO, el=self.text_PO.el_textNote_loc, actionEl=self.text_PO.btn_del_loc)
        #是否删除成功
        self.assertFalse(public_check(self.text_PO, self.text_PO.el_textNote_loc))
        click_trash(self.text_PO)  #打开废纸篓进行恢复
        recovery(self.text_PO)
        #是否恢复成功
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNote_loc))
        #恢复后的数据是否还在
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNoteText_loc, self.textContent))

        public_delProject(self.text_PO, self.home_url)

    def test_shear(self):
        '''剪切，粘贴'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
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

        public_delProject(self.text_PO, self.home_url)

    def test_multiShear(self):
        '''多选剪切，粘贴'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
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

        public_delProject(self.text_PO, self.home_url)

    def test_multiDel(self):
        '''多选删除,恢复'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
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

        public_delProject(self.text_PO, self.home_url)

    def test_drag(self):
        '''拖动到文件夹内'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
        public_addTool(self.text_PO, self.text_PO.tool_text_loc, self.text_PO.el_textNote_loc)
        #是否新建成功
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNote_loc))
        self.text_PO.input_textNote(self.textContent)  #点击文本便签，再输入文本
        #添加文件夹
        public_addTool(self.text_PO, self.text_PO.tool_folder_loc, self.text_PO.el_folder_loc, x=300, y=500)
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_folder_loc))
        #拖动文本便签到文件夹内
        elDrag(self.text_PO, self.text_PO.el_textNote_loc, self.text_PO.el_folder_loc)
        # self.assertFalse(public_check(self.text_PO,self.text_PO.el_textNote_loc))

        public_delProject(self.text_PO, self.home_url)

    def test_copy(self):
        '''复制/粘贴，跨项目'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
        public_addTool(self.text_PO, self.text_PO.tool_text_loc, self.text_PO.el_textNote_loc)
        #是否新建成功
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNote_loc))
        self.text_PO.input_textNote(self.textContent)  #点击文本便签，再输入文本
        #右键-复制
        rightClick_action(self.text_PO, el=self.text_PO.el_textNote_loc, actionEl=self.text_PO.btn_copy_loc)
        #右键-粘贴
        rightClick_action(self.text_PO, 10, 200, self.text_PO.el_textNote_loc, self.text_PO.btn_zhantie_loc)
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNote_loc, islen=True) == 2)
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNoteText_loc, self.textContent))
        sleep(2)
        self.text_PO.driver.get(self.home_url)
        public_createProject(self.text_PO, '[copy]' + self.projectName)
        public_intoProject(self.text_PO)
        rightClick_action(self.text_PO, 300, 200, self.text_PO.svg_loc, self.text_PO.btn_zhantie_loc)
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNote_loc))
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNoteText_loc, self.textContent))

        public_delProject(self.text_PO, self.home_url)

    def test_doubleTextCopy(self):
        '''多文本便签，多选复制/粘贴，跨项目'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
        public_addTool(self.text_PO, self.text_PO.tool_text_loc, self.text_PO.el_textNote_loc, nums=2)
        #是否新建成功
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNote_loc))
        self.text_PO.input_textNote(self.textContent)  #点击文本便签，再输入文本
        selection(self.text_PO, self.text_PO.el_textNote_loc)
        #右键-复制
        rightClick_action(self.text_PO, el=self.text_PO.el_textNote_loc, actionEl=self.text_PO.btn_copy_loc)
        #右键-粘贴
        rightClick_action(self.text_PO, 450, 10, self.text_PO.el_textNote_loc, self.text_PO.btn_zhantie_loc)
        self.assertIs(public_check(self.text_PO, self.text_PO.el_textNote_loc, islen=True), 4)
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNoteText_loc, self.textContent))
        sleep(2)
        self.text_PO.driver.get(self.home_url)
        public_createProject(self.text_PO, '[copy]' + self.projectName)
        public_intoProject(self.text_PO)
        rightClick_action(self.text_PO, 300, 200, self.text_PO.svg_loc, self.text_PO.btn_zhantie_loc)
        self.assertIs(public_check(self.text_PO, self.text_PO.el_textNote_loc, islen=True), 2)
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNoteText_loc, self.textContent))

        public_delProject(self.text_PO, self.home_url)


if __name__ == "__main__":
    unittest.main()
