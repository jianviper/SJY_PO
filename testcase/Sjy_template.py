#!/usr/bin/env python
#coding:utf-8
import unittest
from common.get_config import get_url
from pages.Page_template import TemplatePage
from parts.tool_worker import *
from parts.tool_page import wait_tips

'''
Create on 2020-4-7
author:linjian
summary:模版的测试用例
'''


class InviteTest(unittest.TestCase):
    def setUp(self) -> None:
        urls = get_url()  #return [url,home_url]
        self.url, self.home_url = urls[0], urls[1]
        self.username = '14500000050'
        self.username2 = '14500000051'
        self.password = '123456'
        self.temp_PO = TemplatePage(base_url=self.url)
        self.projectName = project_name()
        self.textContent = textNote_Content()
        self.temp_PO.open()

    def tearDown(self) -> None:
        public_tearDown(self.temp_PO, self.url, self.home_url, self.username, self.password)
        self.temp_PO.driver.quit()

    def test_add_template(self):
        '''添加模板'''
        public_init(self.temp_PO, self.username, self.password, self.projectName)
        self.temp_PO.add_temp()
        self.assertIs(6, public_check(self.temp_PO, self.temp_PO.el_divs_loc, islen=True))

        public_delProject(self.temp_PO, self.home_url)

    def test_search(self):
        '''模板正常搜索'''
        public_init(self.temp_PO, self.username, self.password, self.projectName)
        self.temp_PO.choose_template()
        self.temp_PO.do_search("swot")
        self.assertTrue(public_check(self.temp_PO, self.temp_PO.el_resultName_loc, text='SWOT分析'))

        public_delProject(self.temp_PO, self.home_url)

    def test_submit(self):
        '''模版搜不到，提交自定义模板'''
        public_init(self.temp_PO, self.username, self.password, self.projectName)
        self.temp_PO.choose_template()
        self.temp_PO.do_search("python")  #执行搜索
        self.assertTrue(public_check(self.temp_PO, self.temp_PO.el_secondtext_loc))
        self.temp_PO.click_submit()
        #不输入内容直接点击提交
        self.assertTrue(public_check(self.temp_PO, self.temp_PO.el_warnTitle_loc))
        self.temp_PO.submit_myTemp(self.textContent, "tester")
        wait_tips(self.temp_PO)
        self.temp_PO.click_notfind()  #点击“找不到模板？”
        self.temp_PO.submit_myTemp("2" + self.textContent, "tester", sb=2)
        wait_tips(self.temp_PO)

        public_delProject(self.temp_PO, self.home_url)


if __name__ == '__main__':
    unittest.main()
