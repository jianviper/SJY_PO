#!/usr/bin/env python
#coding:utf-8
import unittest
from common.get_config import get_url
from parts.tool_page import tiyan
from parts.tools_element import ElementTool
from parts.tools_page import PageTool
from pages.Page_worker import WorkerPage
from time import sleep

'''
Create on 2020-9-30
author:linjian
summary:层级设置的测试用例
'''


class InviteTest(unittest.TestCase):
    def setUp(self) -> None:
        urls = get_url()  #return [url,home_url]
        self.url, self.home_url = urls[0], urls[1]
        self.username = '14500000050'
        self.username2 = '14500000051'
        self.password = '123456'
        self.index_PO = WorkerPage(base_url=self.url)
        self.pg = PageTool(self.index_PO)
        self.projectName = self.pg.project_name()
        self.textContent = self.pg.textNote_Content()
        self.ele_tool = ElementTool(self.index_PO)
        self.index_PO.open()

    def tearDown(self) -> None:
        self.pg.public_tearDown(self.url, self.home_url, self.username, self.password)
        self.index_PO.driver.quit()

    def test_single_set(self):
        '''各个元素设置置顶置底操作'''
        self.pg.public_init(self.username, self.password, self.projectName)
        self.ele_tool.ws_add([('t', 1), ('i', 1), ('f', 1), ('file', 1)])
        z_index = self.ele_tool.getCss(self.index_PO.el_divs_loc, 'z-index')
        self.assertTrue(z_index == ['1', '2', '3', '4'])
        #文本便签置顶
        self.ele_tool.rightClick(el=self.index_PO.el_textNote_loc, action=self.index_PO.menu_tUp_loc)
        z_index = self.ele_tool.getCss(self.index_PO.el_divs_loc, 'z-index')
        self.assertTrue(z_index == ['4', '1', '2', '3'])
        #文本便签置底
        self.ele_tool.rightClick(el=self.index_PO.el_textNote_loc, action=self.index_PO.menu_tDown_loc)
        z_index = self.ele_tool.getCss(self.index_PO.el_divs_loc, 'z-index')
        self.assertTrue(z_index == ['1', '2', '3', '4'])
        #图片便签置顶
        self.ele_tool.rightClick(el=self.index_PO.el_imgNote_loc, action=self.index_PO.menu_imgUp_loc)
        z_index = self.ele_tool.getCss(self.index_PO.el_divs_loc, 'z-index')
        self.assertTrue(z_index == ['1', '4', '2', '3'])
        #图片便签置底
        self.ele_tool.rightClick(el=self.index_PO.el_imgNote_loc, action=self.index_PO.menu_imgDown_loc)
        z_index = self.ele_tool.getCss(self.index_PO.el_divs_loc, 'z-index')
        self.assertTrue(z_index == ['2', '1', '3', '4'])
        #文件夹置顶
        self.ele_tool.rightClick(el=self.index_PO.el_folder_loc, action=self.index_PO.menu_fUp_loc)
        z_index = self.ele_tool.getCss(self.index_PO.el_divs_loc, 'z-index')
        self.assertTrue(z_index == ['2', '1', '4', '3'])
        #文件夹置底
        self.ele_tool.rightClick(el=self.index_PO.el_folder_loc, action=self.index_PO.menu_fDown_loc)
        z_index = self.ele_tool.getCss(self.index_PO.el_divs_loc, 'z-index')
        self.assertTrue(z_index == ['3', '2', '1', '4'])
        #文件置顶
        self.ele_tool.rightClick(el=self.index_PO.el_file_loc, action=self.index_PO.menu_wUp_loc)
        z_index = self.ele_tool.getCss(self.index_PO.el_divs_loc, 'z-index')
        self.assertTrue(z_index == ['3', '2', '1', '4'])
        #文件置底
        self.ele_tool.rightClick(el=self.index_PO.el_file_loc, action=self.index_PO.menu_wDown_loc)
        z_index = self.ele_tool.getCss(self.index_PO.el_divs_loc, 'z-index')
        self.assertTrue(z_index == ['4', '3', '2', '1'])

    def test_mutli_set(self):
        '''对多个元素同时设置置顶或置底'''
        self.pg.public_init(self.username, self.password, self.projectName)
        self.ele_tool.ws_add([('t', 1), ('i', 1), ('f', 1), ('file', 1)])
        z_index = self.ele_tool.getCss(self.index_PO.el_divs_loc, 'z-index')
        self.assertTrue(z_index == ['1', '2', '3', '4'])
        self.ele_tool.selection(self.index_PO.el_divs_loc)
        #多选后设置置顶
        self.ele_tool.rightClick(el=self.index_PO.el_textNote_loc, action=self.index_PO.menu_tUp_loc)
        z_index = self.ele_tool.getCss(self.index_PO.el_divs_loc, 'z-index')
        self.assertTrue(z_index == ['1', '2', '3', '4'])
        self.ele_tool.selection(self.index_PO.el_divs_loc)
        #多选后设置置底
        self.ele_tool.rightClick(el=self.index_PO.el_textNote_loc, action=self.index_PO.menu_tDown_loc)
        z_index = self.ele_tool.getCss(self.index_PO.el_divs_loc, 'z-index')
        self.assertTrue(z_index == ['1', '2', '3', '4'])


if __name__ == '__main__':
    unittest.main()
