#!/usr/bin/env python
#coding:utf-8
from selenium.webdriver.common.by import By
from common.BasePage import BasePage
from time import sleep

'''
Create on 2020-3-18
author:linjian
summary:Home页的元素对象
'''


class HomePage(BasePage):
    #定位器，通过元素属性定位元素对象
    helpButton_loc = (By.CLASS_NAME, 'guideHelp')
    userButton_loc = (By.CLASS_NAME, 'menu_user')
    userMenu_loc = (By.CLASS_NAME, 'meny_level2')
    createProject_loc = (By.CSS_SELECTOR, '.header_add.ant-btn.ant-btn-default')
    projectName_loc = (By.CLASS_NAME, 'ant-input')
    CPSubmitButton_loc = (By.CSS_SELECTOR, '.footer_submit.ant-btn.ant-btn-default')
    firstProjectMenu_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:first-child>.item_set>img')
    renameProjectMenu_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:first-child>.item_menu>:first-child')
    lastProjectName_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:last-child>.item_text>.item_title')
    lastProjectMenu_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:last-child>.item_set>img')
    delMenuButton_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:last-child>ul>:last-child')
    delProjectName_loc = (By.CSS_SELECTOR, '.header_subtitle>span')
    inputProjectName_loc = (By.CSS_SELECTOR, '.form_item>input[type=text]')
    delSubmitButton_loc = (By.CSS_SELECTOR, '.footer_submit.ant-btn.ant-btn-default')
    Tips_loc = (By.XPATH, '//*[@class="ant-message"]/span//span')
    item_menuNum = (By.CSS_SELECTOR, '.home_content.clearfix>div')
    firstProject_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:first-child')

    #通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    #打开网页
    def open(self):
        self._open(self.baseurl)

    def go_helpPage(self):
        self.find_element(*self.helpButton_loc).click()

    def go_userMenu(self):
        self.find_element(*self.userButton_loc).click()

    def check_userMenu(self):
        return self.find_element(*self.userMenu_loc)

    def click_createProject(self):
        print(self.find_element(*self.createProject_loc))
        self.find_element(*self.createProject_loc).click()

    def input_create_projectName(self, name):
        self.find_element(*self.projectName_loc).send_keys(name)

    def click_CPSubmit(self):
        self.find_element(*self.CPSubmitButton_loc).click()
        sleep(1)

    def get_lastProjectName(self):
        return self.find_element(*self.lastProjectName_loc).text

    def click_lastProjectMenu(self):
        self.find_element(*self.lastProjectMenu_loc).click()

    def click_firstProjectMenu(self):
        self.find_element(*self.firstProjectMenu_loc).click()

    def click_delButton(self):
        self.find_element(*self.delMenuButton_loc).click()
        sleep(1)

    def click_renameButton(self):
        self.find_element(*self.renameProjectMenu_loc).click()

    def input_projectName(self, name=''):
        name = name
        if name=='':
            name = self.find_element(*self.delProjectName_loc).text
        # print(name)
        self.find_element(*self.inputProjectName_loc).send_keys(name)

    def click_delSubmitButton(self):
        self.find_element(*self.delSubmitButton_loc).click()

    def get_tips(self):
        return self.find_element(*self.Tips_loc).text

    def get_projectNum(self):
        num=self.driver.find_elements(*self.item_menuNum).__len__()
        return num

    def click_firstProject(self):
        self.find_element(*self.firstProject_loc).click()
