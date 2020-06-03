#!/usr/bin/env python
#coding:utf-8
import unittest
from common.get_config import get_url
from pages.Page_worker import WorkerPage
from parts.tool_worker import *
from parts.ws_client import WSupload_img

'''
Create on 2020-5-29
author:linjian
summary:关联线的测试用例
'''


class LinkTest(unittest.TestCase):

    def setUp(self) -> None:
        urls = get_url()  #return [url,home_url]
        self.url, self.home_url = urls[0], urls[1]
        self.username = '14500000050'
        self.username2 = '14500000051'
        self.password = '123456'
        self.link_PO = WorkerPage(base_url=self.url)
        self.projectName = project_name()
        self.textContent = textNote_Content()
        self.link_PO.open()

    def tearDown(self) -> None:
        # public_tearDown(self.link_PO, self.url, self.home_url, self.username, self.password)
        self.link_PO.driver.quit()

    def test_link(self):
        public_login(self.link_PO, self.username, self.password)
        public_intoProject(self.link_PO)
        left_click(self.link_PO, el=self.link_PO.el_textNote_loc)
        sleep(2)
        elDrag(self.link_PO, self.link_PO.el_linkPoint_loc, self.link_PO.el_imgDIV_loc)
        # drag_and_drop(self.link_PO)

        sleep(10)

    def test_textAndimg(self):
        '''文本便签和图片便签的组合关联线'''
        public_init(self.link_PO, self.username, self.password, self.projectName)
        public_addTool(self.link_PO, self.link_PO.tool_text_loc, self.link_PO.el_textNote_loc)
        self.link_PO.input_textNote(self.textContent)
        public_addTool(self.link_PO, self.link_PO.tool_img_loc, self.link_PO.el_imgDIV_loc, x=200, y=300)
        WSupload_img(self.link_PO, self.link_PO.el_imgDIV_loc, 'data-id')
        self.link_PO.driver.refresh()
        #是否新建成功
        self.assertTrue(public_check(self.link_PO, self.link_PO.el_img_loc, attr='src'))
        self.assertTrue(public_check(self.link_PO, self.link_PO.el_textNote_loc))
        left_click(self.link_PO, el=self.link_PO.el_textNote_loc)
        elDrag(self.link_PO, self.link_PO.el_linkPoint_loc, self.link_PO.el_imgDIV_loc)

        assert False
        #框选，右键剪切，粘贴
        selection(self.link_PO, [self.link_PO.el_textNote_loc, self.link_PO.el_imgDIV_loc])
        rightClick_action(self.link_PO, el=self.link_PO.el_imgDIV_loc, actionEl=self.link_PO.btn_jianqie_loc)
        left_click(self.link_PO, 50, -80, self.link_PO.tool_mouse_loc)
        self.assertIs(public_check(self.link_PO, self.link_PO.el_divs_loc, islen=True), 2)
        rightClick_action(self.link_PO, 200, 10, self.link_PO.tool_loc, actionEl=self.link_PO.btn_zhantie_loc)
        #检查是否粘贴成功
        self.assertTrue(public_check(self.link_PO, self.link_PO.el_img_loc, attr='src'))
        self.assertTrue(public_check(self.link_PO, self.link_PO.el_textNote_loc))
        #框选，右键复制，粘贴
        selection(self.link_PO, [self.link_PO.el_textNote_loc, self.link_PO.el_imgDIV_loc])
        rightClick_action(self.link_PO, el=self.link_PO.el_imgDIV_loc, actionEl=self.link_PO.btn_copy_loc)
        left_click(self.link_PO, 50, -80, self.link_PO.tool_mouse_loc)
        self.assertIs(public_check(self.link_PO, self.link_PO.el_divs_loc, islen=True), 4)
        rightClick_action(self.link_PO, 200, 400, self.link_PO.tool_loc, actionEl=self.link_PO.btn_zhantie_loc)
        #检查是否粘贴成功
        self.assertTrue(public_check(self.link_PO, self.link_PO.el_img_loc, attr='src'))
        self.assertIs(public_check(self.link_PO, self.link_PO.el_textNote_loc, islen=True), 2)

        public_delProject(self.link_PO, self.home_url)

    def test_textAndfolder(self):
        '''文本便签和文件夹的组合剪切粘贴，复制粘贴的操作'''
        public_init(self.link_PO, self.username, self.password, self.projectName)
        public_addTool(self.link_PO, self.link_PO.tool_text_loc, self.link_PO.el_textNote_loc)
        self.link_PO.input_textNote(self.textContent)
        public_addTool(self.link_PO, self.link_PO.tool_folder_loc, self.link_PO.el_folder_loc, x=200, y=300)
        #是否新建成功
        self.assertTrue(public_check(self.link_PO, self.link_PO.el_folder_loc))
        self.assertTrue(public_check(self.link_PO, self.link_PO.el_textNote_loc))
        #框选，右键剪切，粘贴
        selection(self.link_PO, [self.link_PO.el_textNote_loc, self.link_PO.el_folder_loc])
        rightClick_action(self.link_PO, el=self.link_PO.el_folder_loc, actionEl=self.link_PO.btn_fjianqie_loc)
        left_click(self.link_PO, 50, -80, self.link_PO.tool_mouse_loc)
        self.assertIs(public_check(self.link_PO, self.link_PO.el_divs_loc, islen=True), 2)
        rightClick_action(self.link_PO, 200, 10, self.link_PO.tool_loc, actionEl=self.link_PO.btn_zhantie_loc)
        #检查是否粘贴成功
        self.assertTrue(public_check(self.link_PO, self.link_PO.el_folder_loc))
        self.assertTrue(public_check(self.link_PO, self.link_PO.el_textNote_loc))
        #框选，右键复制，粘贴
        selection(self.link_PO, [self.link_PO.el_textNote_loc, self.link_PO.el_folder_loc])
        rightClick_action(self.link_PO, el=self.link_PO.el_folder_loc, actionEl=self.link_PO.btn_fcopy_loc)
        left_click(self.link_PO, 50, -80, self.link_PO.tool_mouse_loc)
        self.assertIs(public_check(self.link_PO, self.link_PO.el_divs_loc, islen=True), 4)
        rightClick_action(self.link_PO, 200, 400, self.link_PO.tool_loc, actionEl=self.link_PO.btn_zhantie_loc)
        #检查是否粘贴成功
        self.assertIs(public_check(self.link_PO, self.link_PO.el_folder_loc, islen=True), 2)
        self.assertIs(public_check(self.link_PO, self.link_PO.el_textNote_loc, islen=True), 2)

        public_delProject(self.link_PO, self.home_url)

    def test_imgAndfolder(self):
        '''图片便签和文件夹的组合剪切粘贴，复制粘贴的操作'''
        public_init(self.link_PO, self.username, self.password, self.projectName)
        public_addTool(self.link_PO, self.link_PO.tool_img_loc, self.link_PO.el_imgDIV_loc)
        WSupload_img(self.link_PO, self.link_PO.el_imgDIV_loc, 'data-id')
        public_addTool(self.link_PO, self.link_PO.tool_folder_loc, self.link_PO.el_folder_loc, x=200, y=300)
        self.link_PO.driver.refresh()
        #是否新建成功
        self.assertTrue(public_check(self.link_PO, self.link_PO.el_img_loc, attr='src'))
        self.assertTrue(public_check(self.link_PO, self.link_PO.el_folder_loc))
        #框选，右键剪切，粘贴
        selection(self.link_PO, [self.link_PO.el_folder_loc, self.link_PO.el_imgDIV_loc])
        rightClick_action(self.link_PO, el=self.link_PO.el_imgDIV_loc, actionEl=self.link_PO.btn_jianqie_loc)
        left_click(self.link_PO, 50, -80, self.link_PO.tool_mouse_loc)
        self.assertIs(public_check(self.link_PO, self.link_PO.el_divs_loc, islen=True), 2)
        rightClick_action(self.link_PO, 200, 10, self.link_PO.tool_loc, actionEl=self.link_PO.btn_zhantie_loc)
        #检查是否粘贴成功
        self.assertTrue(public_check(self.link_PO, self.link_PO.el_img_loc, attr='src'))
        self.assertTrue(public_check(self.link_PO, self.link_PO.el_folder_loc))
        #框选，右键复制，粘贴
        selection(self.link_PO, [self.link_PO.el_folder_loc, self.link_PO.el_imgDIV_loc])
        rightClick_action(self.link_PO, el=self.link_PO.el_imgDIV_loc, actionEl=self.link_PO.btn_copy_loc)
        left_click(self.link_PO, 50, -80, self.link_PO.tool_mouse_loc)
        self.assertIs(public_check(self.link_PO, self.link_PO.el_divs_loc, islen=True), 4)
        rightClick_action(self.link_PO, 200, 400, self.link_PO.tool_loc, actionEl=self.link_PO.btn_zhantie_loc)
        #检查是否粘贴成功
        self.assertTrue(public_check(self.link_PO, self.link_PO.el_img_loc, attr='src'))
        self.assertIs(public_check(self.link_PO, self.link_PO.el_folder_loc, islen=True), 2)

        public_delProject(self.link_PO, self.home_url)

    def test_textAndimg2(self):
        '''文本便签和图片便签的组合,挨个剪切，再粘贴，挨个复制再粘贴的操作'''
        public_init(self.link_PO, self.username, self.password, self.projectName)
        public_addTool(self.link_PO, self.link_PO.tool_text_loc, self.link_PO.el_textNote_loc)
        self.link_PO.input_textNote(self.textContent)
        public_addTool(self.link_PO, self.link_PO.tool_img_loc, self.link_PO.el_imgDIV_loc, x=200, y=300)
        WSupload_img(self.link_PO, self.link_PO.el_imgDIV_loc, 'data-id')
        self.link_PO.driver.refresh()
        #是否新建成功
        self.assertTrue(public_check(self.link_PO, self.link_PO.el_img_loc, attr='src'))
        self.assertTrue(public_check(self.link_PO, self.link_PO.el_textNote_loc))
        #框选，右键剪切，粘贴
        selection(self.link_PO, [self.link_PO.el_textNote_loc, self.link_PO.el_imgDIV_loc])
        rightClick_action(self.link_PO, el=self.link_PO.el_imgDIV_loc, actionEl=self.link_PO.btn_jianqie_loc)
        left_click(self.link_PO, 50, -80, self.link_PO.tool_mouse_loc)
        self.assertIs(public_check(self.link_PO, self.link_PO.el_divs_loc, islen=True), 2)
        rightClick_action(self.link_PO, 200, 10, self.link_PO.tool_loc, actionEl=self.link_PO.btn_zhantie_loc)
        #检查是否粘贴成功
        self.assertTrue(public_check(self.link_PO, self.link_PO.el_img_loc, attr='src'))
        self.assertTrue(public_check(self.link_PO, self.link_PO.el_textNote_loc))
        #框选，右键复制，粘贴
        selection(self.link_PO, [self.link_PO.el_textNote_loc, self.link_PO.el_imgDIV_loc])
        rightClick_action(self.link_PO, el=self.link_PO.el_imgDIV_loc, actionEl=self.link_PO.btn_copy_loc)
        left_click(self.link_PO, 50, -80, self.link_PO.tool_mouse_loc)
        self.assertIs(public_check(self.link_PO, self.link_PO.el_divs_loc, islen=True), 4)
        rightClick_action(self.link_PO, 200, 400, self.link_PO.tool_loc, actionEl=self.link_PO.btn_zhantie_loc)
        #检查是否粘贴成功
        self.assertTrue(public_check(self.link_PO, self.link_PO.el_img_loc, attr='src'))
        self.assertIs(public_check(self.link_PO, self.link_PO.el_textNote_loc, islen=True), 2)

        public_delProject(self.link_PO, self.home_url)


if __name__ == "__main__":
    unittest.main()
