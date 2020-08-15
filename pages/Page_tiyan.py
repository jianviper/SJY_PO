#!/usr/bin/env python
#coding:utf-8
from selenium.webdriver.common.by import By
from common.BasePage import BasePage
from time import sleep

'''
Create on 2020-6-3
author:linjian
summary:体验功能的元素对象
'''


class TiyanPage(BasePage):
    #定位器，通过元素属性定位元素对象
    svg_loc = (By.XPATH, '//*[@class="svg_content"]')

    tool_loc = (By.CLASS_NAME, 'work_tool')

    el_codeimg_loc = (By.CLASS_NAME, 'code_image')
    el_title_loc = (By.CLASS_NAME, 'info_title1')
    el_course_loc = (By.CLASS_NAME, 'course')

    btn_menusign_loc = (By.CLASS_NAME, 'menu_login')
    btn_invite_loc = (By.CLASS_NAME, 'userout')
    btn_sign_loc = (By.CSS_SELECTOR, '.sure-btn.submit-info')
    btn_next_loc = (By.CLASS_NAME, 'button_next')
    btn_finish_loc = (By.CLASS_NAME, 'button_adopt')
    btn_skip_loc = (By.CLASS_NAME, 'button_skip')

    lastProjectName_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:last-child>.item_text>.item_title')

    #通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    #打开网页
    def open(self):
        self._open(self.baseurl)

    def click_menuSign(self):
        self.find_element(*self.btn_menusign_loc).click()
        sleep(2)

    def click_invite(self):
        self.find_element(*self.btn_invite_loc).click()
        sleep(2)

    def click_sign(self):
        self.find_element(*self.btn_sign_loc).click()
        sleep(2)

    def click_next(self):
        self.find_element(*self.btn_next_loc).click()

    def get_title(self, el):
        return self.find_element(*el).text

    def click_finish(self):
        self.find_element(*self.btn_finish_loc).click()

    def click_skip(self):
        self.find_element(*self.btn_skip_loc).click()
