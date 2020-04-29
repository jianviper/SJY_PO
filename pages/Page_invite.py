#!/usr/bin/env python
#coding:utf-8
from selenium.webdriver.common.by import By
from common.BasePage import BasePage
from time import sleep

'''
Create on 2020-3-18
author:linjian
summary:邀请/加入功能的元素对象
'''


class InvitePage(BasePage):
    #定位器，通过元素属性定位元素对象
    btn_invite_loc = (By.CLASS_NAME, 'menbercompoment')
    btn_joinInvi_loc=(By.CSS_SELECTOR,'.invitation_submit.sure-btn')
    btn_user_loc=(By.CLASS_NAME,'user_box')
    btn_exit_loc=(By.CSS_SELECTOR,'.team_invitation>button')
    btn_exitSure_loc=(By.CSS_SELECTOR,'.footer_submit.ant-btn')

    inviUrl_loc = (By.ID, 'inviUrl')
    inviName_loc=(By.CSS_SELECTOR, '.invitation_content>p>span:last-child')
    lastProjectName_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:last-child>.item_text>.item_title')

    #通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    #打开网页
    def open(self):
        self._open(self.baseurl)

    def click_invite(self):
        self.find_element(*self.btn_invite_loc).click()

    def get_inviUrl(self):
        return self.find_element(*self.inviUrl_loc).get_attribute('value')

    def click_joinInvi(self):
        self.find_element(*self.btn_joinInvi_loc).click()

    def get_inviName(self):
        return self.find_element(*self.inviName_loc).text

    def exit_project(self):
        self.find_element(*self.btn_user_loc).click()
        self.find_element(*self.btn_exit_loc).click()
        self.find_element(*self.btn_exitSure_loc).click()
        sleep(2)