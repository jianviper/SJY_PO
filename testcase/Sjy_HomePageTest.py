#!/usr/bin/env python
#coding:utf-8
import unittest
from time import strftime,localtime
from pages.Page_Home import HomePage
from parts.pageTools import *
'''
Create on 2020-3-17
author:linjian
summary:Home页的测试用例
'''


class HomeTest(unittest.TestCase):
    def setUp(self) -> None:
        url = 'https://app.bimuyu.tech/login'
        self.username = '14500000050'
        self.password = '123456'
        self.homePage = HomePage(base_url=url)
        self._nowtime = strftime("%Y-%m-%d %H:%M:%S", localtime())
        self.projectName = '自动化测试项目-{0}'.format(self._nowtime)
        self.homePage.open()

    def tearDown(self) -> None:
        self.homePage.driver.quit()

    def test_helpPage(self):
        '''新手教程页打开是否正常'''
        public_login(self.homePage, self.username, self.password)
        self.homePage.go_helpPage()
        self.homePage.driver.switch_to.window(self.homePage.driver.window_handles[1])
        self.assertEqual('比幕鱼 - 新手教程', self.homePage.driver.title)

    def test_userMenu(self):
        '''用户个人中心菜单打开是否正常'''
        public_login(self.homePage, self.username, self.password)
        self.homePage.go_userMenu()
        self.assertTrue(self.homePage.check_userMenu())

    def test_createProject(self):
        '''正常创建项目测试'''
        public_login(self.homePage, self.username, self.password)
        self.homePage.createProject(self.projectName)
        self.assertEqual(self.projectName, self.homePage.get_lastProjectName())
        sleep(2)

    def test_projectNameRename(self):
        '''项目名称重命名'''
        public_login(self.homePage, self.username, self.password)
        while self.homePage.get_projectNum() == 0:
            self.homePage.createProject(self.projectName)  #新建项目
            self.assertEqual(self.projectName, self.homePage.get_lastProjectName())
            self.homePage.driver.refresh()
            sleep(1)
        self.homePage.click_firstProjectMenu()
        self.homePage.click_renameButton()
        self.homePage.input_projectName(self.projectName)
        self.homePage.click_CRDSubmit()
        self.assertEqual('成功', self.homePage.get_tips())

    def test_delProject(self):
        '''删除项目'''
        public_login(self.homePage, self.username, self.password)
        # self.HomePage.driver.switch_to.window(self.HomePage.driver.window_handles[0])
        while self.homePage.get_projectNum() == 0:
            self.homePage.createProject(self.projectName)  #新建项目
            self.assertEqual(self.projectName, self.homePage.get_lastProjectName())
            self.homePage.driver.refresh()
            sleep(1)
        self.homePage.click_lastProjectMenu()
        self.homePage.click_delButton()
        self.homePage.input_projectName(d=True)
        self.homePage.click_CRDSubmit()
        self.assertEqual('成功', self.homePage.get_tips())

if __name__ == "__main__":
    unittest.main()
