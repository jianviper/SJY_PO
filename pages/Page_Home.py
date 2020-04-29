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
    menu_user_loc = (By.CLASS_NAME, 'meny_level2')  #头像点击菜单
    delProjectName_loc = (By.CSS_SELECTOR, '.header_subtitle>span')  #删除要确认的名称
    Tips_loc = (By.XPATH, '//*[@class="ant-message"]/span//span')
    num_project_loc = (By.CSS_SELECTOR, '.home_content.clearfix>div')  #项目数量
    firstProject_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:first-child')  #第一个项目
    win_bind_loc = (By.CLASS_NAME, 'ant-modal-body')  #
    input_projectName_loc = (By.CLASS_NAME, 'ant-input')
    input_delPJName_loc = (By.CSS_SELECTOR, '.form_item.form-line>input')

    btn_help_loc = (By.CLASS_NAME, 'guideHelp')
    btn_user_loc = (By.CSS_SELECTOR, '.menu_user.mouse_hover')
    btn_createProject_loc = (By.CSS_SELECTOR, '.header_add.ant-btn')
    #CRD:创建，重命名，删除 按钮
    btn_CRD_loc = (By.CSS_SELECTOR, '.sure-btn.ant-btn')
    btn_projectMenu_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:first-child>.item_set>img')
    btn_menu_rename_loc = (By.CSS_SELECTOR, '.item_menu>li:first-child')
    btn_menu_del_loc = (By.CSS_SELECTOR, '.item_menu>li:last-child')
    btn_closeBind_loc = (By.CLASS_NAME, 'closeBtn')

    lastProjectName_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:last-child>.item_text>.item_title')
    lastProjectMenu_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:last-child>.item_set>img')

    #通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    #打开网页
    def open(self):
        self._open(self.baseurl)

    def go_helpPage(self):
        self.find_element(*self.btn_help_loc).click()

    def go_userMenu(self):
        self.find_element(*self.btn_user_loc).click()

    def check_userMenu(self):
        return self.find_element(*self.menu_user_loc)

    def click_createProject(self):
        #点击"新建项目"
        self.find_element(*self.btn_createProject_loc).click()

    def input_create_projectName(self, name):
        self.find_element(*self.input_projectName_loc).send_keys(name)

    def click_CRDSubmit(self):
        #创建，重命名，删除确定按钮
        self.find_element(*self.btn_CRD_loc).click()
        sleep(1)

    def get_lastProjectName(self):
        #获取最后一个项目的名称
        return self.find_element(*self.lastProjectName_loc).text

    def click_lastProjectMenu(self):
        self.find_element(*self.lastProjectMenu_loc).click()

    def click_firstProjectMenu(self):
        #第一个项目的右上角menu
        self.find_element(*self.btn_projectMenu_loc).click()

    def click_delButton(self):
        self.find_element(*self.btn_menu_del_loc).click()
        sleep(1)

    def click_renameButton(self):
        self.find_element(*self.btn_menu_rename_loc).click()

    def input_projectName(self, name='', d=None):
        #d:删除标记
        name = name
        if name == '' and d:
            name = self.find_element(*self.delProjectName_loc).text
            self.find_element(*self.input_delPJName_loc).send_keys(name)
            return True
        # print(name)
        self.find_element(*self.input_projectName_loc).send_keys(name)

    def get_tips(self):
        return self.find_element(*self.Tips_loc).text

    def get_projectNum(self):
        num = self.driver.find_elements(*self.num_project_loc).__len__()
        return num

    def click_firstProject(self):
        self.find_element(*self.firstProject_loc).click()

    def createProject(self, name):
        '''创建项目'''
        self.click_createProject()
        self.input_create_projectName(name)
        self.click_CRDSubmit()
