#!/usr/bin/env python
#coding:utf-8
import unittest
from common.get_config import get_url
from pages.Page_worker import WorkerPage
from parts.tools_element import ElementTool
from parts.tools_page import PageTool

'''
Create on 2020-10-15
author:linjian
summary:导出测试用例
'''


class Export(unittest.TestCase):
    def setUp(self) -> None:
        urls = get_url()  #return [url,home_url]
        self.url, self.home_url = urls[0], urls[1]
        self.username = '14500000050'
        self.password = '123456'
        self.ex_PO = WorkerPage(base_url=self.url)
        self.pg = PageTool(self.ex_PO)
        self.projectName = self.pg.project_name()
        self.ele_tool = ElementTool(self.ex_PO)
        self.ex_PO.open()

    def tearDown(self) -> None:
        self.pg.public_tearDown(self.url, self.home_url, self.username, self.password)
        self.ex_PO.driver.quit()

    def test_page_export(self):
        '''本页导出'''
        self.pg.public_init(self.username, self.password, self.projectName)
        self.ele_tool.ws_add('all')
        self.ex_PO.page_export()
        self.pg.wait_tips(self.ex_PO.tip_page_export_loc, sec=1, max=10)
        self.assertTrue(self.ex_PO.check_file(self.projectName.replace(':', '_')))

    def test_selection_export(self):
        '''框选元素导出'''
        self.pg.public_init(self.username, self.password, self.projectName)
        self.ele_tool.ws_add('all')
        self.ele_tool.selection(self.ex_PO.el_divs_loc)
        self.ele_tool.rightClick(el=self.ex_PO.el_textNote_loc, action=self.ex_PO.menu_export_loc)
        self.pg.wait_tips(self.ex_PO.tip_select_export_loc, sec=1, max=10)
        self.assertTrue(self.ex_PO.check_file(self.projectName.replace(':', '_')))


if __name__ == '__main__':
    unittest.main()
