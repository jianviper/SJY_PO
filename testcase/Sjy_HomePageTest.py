#!/usr/bin/env python
#coding:utf-8
import unittest
from common.get_config import get_url
from pages.Page_Home import HomePage
from parts.tool_page import *

'''
Create on 2020-3-17
author:linjian
summary:Home页的测试用例
'''


class HomeTest(unittest.TestCase):
    def setUp(self) -> None:
        urls = get_url()  #return [url,home_url]
        self.url, self.home_url = urls[0], urls[1]
        self.username = '14500000050'
        self.password = '123456'
        self.hp_PO = HomePage(base_url=self.url)
        self.projectName = project_name()
        self.hp_PO.open()

    def tearDown(self) -> None:
        public_tearDown(self.hp_PO, self.url, self.home_url, self.username, self.password)
        self.hp_PO.driver.quit()

    def test_helpPage(self):
        '''新手教程页打开是否正常'''
        public_login(self.hp_PO, self.username, self.password)
        self.hp_PO.go_helpPage()
        self.hp_PO.driver.switch_to.window(self.hp_PO.driver.window_handles[1])
        self.assertEqual('比幕鱼 - 新手教程', self.hp_PO.driver.title)

    def test_userMenu(self):
        '''用户个人中心菜单打开是否正常'''
        public_login(self.hp_PO, self.username, self.password)
        self.hp_PO.go_userMenu()
        self.assertTrue(self.hp_PO.check_userMenu())

    def test_createProject(self):
        '''正常创建项目测试'''
        public_login(self.hp_PO, self.username, self.password)
        self.hp_PO.createProject(self.projectName)
        self.assertEqual(self.projectName, self.hp_PO.get_lastProjectName())
        sleep(2)

    def test_projectNameRename(self):
        '''项目名称重命名'''
        public_login(self.hp_PO, self.username, self.password)
        while self.hp_PO.get_projectNum() == 0:
            self.hp_PO.createProject(self.projectName)  #新建项目
            self.assertEqual(self.projectName, self.hp_PO.get_lastProjectName())
            self.hp_PO.driver.refresh()
            sleep(1)
        self.hp_PO.click_lastProjectMenu()
        self.hp_PO.click_renameButton()
        self.hp_PO.input_projectName("[rename]" + self.projectName)
        self.hp_PO.click_CRDSubmit()
        self.assertEqual("[rename]" + self.projectName, self.hp_PO.get_lastProjectName())
        self.assertEqual('修改成功', self.hp_PO.get_tips())

    def test_delProject(self):
        '''删除项目'''
        public_login(self.hp_PO, self.username, self.password)
        # self.HomePage.driver.switch_to.window(self.HomePage.driver.window_handles[0])
        while self.hp_PO.get_projectNum() == 0:
            self.hp_PO.createProject(self.projectName)  #新建项目
            self.assertEqual(self.projectName, self.hp_PO.get_lastProjectName())
            self.hp_PO.driver.refresh()
            sleep(1)
        self.hp_PO.click_lastProjectMenu()
        self.hp_PO.click_delButton()
        self.hp_PO.input_projectName(d=True)
        self.hp_PO.click_CRDSubmit()
        self.assertEqual('删除成功', self.hp_PO.get_tips())


if __name__ == "__main__":
    unittest.main()
