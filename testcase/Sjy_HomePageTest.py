#!/usr/bin/env python
#coding:utf-8
import unittest
from time import sleep, asctime
from pages.Page_Home import HomePage
from parts.login_ps import publicLogin
from parts.homePage_ps import createProject
'''
Create on 2020-3-17
author:linjian
summary:Home页的测试用例
'''


class HomeTest(unittest.TestCase):
    def setUp(self) -> None:
        url = 'https://app.bimuyu.tech/login'
        self.username = '14500000005'
        self.password = '123456'
        self.HomePage = HomePage(base_url=url)
        self.projectName = '自动化测试项目-{0}'.format(asctime())

    def tearDown(self) -> None:
        self.HomePage.driver.quit()

    def te1st_helpPage(self):
        '''新手教程页打开是否正常'''
        publicLogin(self.HomePage, self.username, self.password)
        self.HomePage.go_helpPage()
        self.HomePage.driver.switch_to.window(self.HomePage.driver.window_handles[1])
        self.assertEqual('比幕鱼 - 新手教程', self.HomePage.driver.title)

    def te1st_userMenu(self):
        '''用户个人中心菜单打开是否正常'''
        publicLogin(self.HomePage, self.username, self.password)
        self.HomePage.go_userMenu()
        self.assertTrue(self.HomePage.check_userMenu())

    def te1st_createProject(self):
        '''正常创建项目测试'''
        publicLogin(self.HomePage, self.username, self.password)
        createProject(self.HomePage,self.projectName)
        self.assertEqual(self.projectName, self.HomePage.get_lastProjectName())
        sleep(2)

    def test_projectNameRename(self):
        '''项目名称重命名'''
        publicLogin(self.HomePage, self.username, self.password)
        while self.HomePage.get_projectNum() == 0:
            createProject(self.HomePage,self.projectName)  #新建项目
            self.assertEqual(self.projectName, self.HomePage.get_lastProjectName())
            self.HomePage.driver.refresh()
            sleep(1)
        self.HomePage.click_firstProjectMenu()
        self.HomePage.click_renameButton()
        self.HomePage.input_projectName(self.projectName)
        self.HomePage.click_CPSubmit()
        self.assertEqual('成功', self.HomePage.get_tips())

    def te1st_delProject(self):
        '''删除项目'''
        publicLogin(self.HomePage, self.username, self.password)
        # self.HomePage.driver.switch_to.window(self.HomePage.driver.window_handles[0])
        while self.HomePage.get_projectNum() == 0:
            createProject(self.HomePage,self.projectName)  #新建项目
            self.assertEqual(self.projectName, self.HomePage.get_lastProjectName())
            self.HomePage.driver.refresh()
            sleep(1)
        self.HomePage.click_lastProjectMenu()
        self.HomePage.click_delButton()
        self.HomePage.input_projectName()
        self.HomePage.click_delSubmitButton()
        self.assertEqual('成功', self.HomePage.get_tips())

if __name__ == "__main__":
    unittest.main()
