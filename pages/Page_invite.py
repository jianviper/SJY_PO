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
    svg_loc = (By.XPATH, '//*[@class="svg_content"]')

    tool_loc = (By.CLASS_NAME, 'work_tool')
    tool_text_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(5)')
    tool_forlder_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(8)')
    el_text_loc = (By.CSS_SELECTOR, '.work_text.work_element')
    el_forlder_loc = (By.CSS_SELECTOR, '.work_file.work_element')

    btn_invite_loc = (By.CLASS_NAME, 'userout')
    btn_role_loc = (By.CLASS_NAME, 'menu')
    btn_reader_loc = (By.CSS_SELECTOR, '.menu>.menu_box>li:last-child')
    btn_joinInvi_loc = (By.CSS_SELECTOR, '.invitation_submit.sure-btn')
    btn_user_loc = (By.CLASS_NAME, 'user_box')
    btn_exit_loc = (By.CSS_SELECTOR, '.team_invitation>button')
    btn_exitSure_loc = (By.CSS_SELECTOR, '.sure-btn.submit-info')

    invite_url_loc = (By.ID, 'inviUrl')
    invite_name_loc = (By.CSS_SELECTOR, '.invitation_content>p>span:last-child')
    lastProjectName_loc = (By.CSS_SELECTOR, '.home_content>:last-child>.item_text>.item_title')

    #通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    #打开网页
    def open(self):
        self._open(self.baseurl)

    def click_invite(self):
        self.find_element(*self.btn_invite_loc).click()

    def choose_reader(self):
        self.find_element(*self.btn_role_loc).click()
        sleep(1)
        self.find_element(*self.btn_reader_loc).click()
        sleep(2)

    def get_inviUrl(self):
        return self.find_element(*self.invite_url_loc).get_attribute('value')

    def click_joinInvi(self):
        self.find_element(*self.btn_joinInvi_loc).click()

    def get_inviName(self):  #获取协同项目名称
        return self.find_element(*self.invite_name_loc).text

    def exit_project(self):  #退出画布
        sleep(1)
        self.find_element(*self.btn_user_loc).click()
        self.find_element(*self.btn_exit_loc).click()
        self.find_element(*self.btn_exitSure_loc).click()
        sleep(2)
