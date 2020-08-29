#!/usr/bin/env python
#coding:utf-8
import unittest
from common.get_config import get_url
from pages.Page_worker import WorkerPage
from parts.tool_worker import *
from common.ws_client import WSupload_img

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
        public_init(self.link_PO, self.username, self.password, self.projectName)
        public_add(self.link_PO, [('t', 1), ('f', 1)])
        # self.link_PO.driver.refresh()
        self.assertTrue(public_check(self.link_PO, self.link_PO.el_divs_loc))
        self.link_PO.click(self.link_PO.el_textNote_loc)
        elDrag(self.link_PO, start=self.link_PO.btn_relbtm_loc, end=self.link_PO.el_folder_loc)
        # self.link_PO.driver.refresh()

        sleep(5)


if __name__ == "__main__":
    unittest.main()
