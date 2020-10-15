#!/usr/bin/env python
#coding:utf-8
from selenium.webdriver.common.by import By
from common.BasePage import BasePage
from time import sleep

'''
Create on 2020-8-19
author:linjian
summary:分享的元素对象
'''


class SharePage(BasePage):
    #定位器，通过元素属性定位元素对象
    tool_loc = (By.CLASS_NAME, 'work_tool')
    header_loc = (By.CSS_SELECTOR, '.header.ant-layout-header')
    code_image_loc = (By.CLASS_NAME, 'code_image')
    first_proTitle_loc = (By.CSS_SELECTOR, '.home_content>:first-child>.item_text>.item_title')
    last_proTitle_loc = (By.CSS_SELECTOR, '.home_content>:last-child>.item_text>.item_title')

    el_divs_loc = (By.CSS_SELECTOR, '.work_element')
    el_shareUrl_loc = (By.ID, 'shareUrl')
    el_save_text_loc = (By.CLASS_NAME, 'save_text')
    el_wb_loc = (By.CSS_SELECTOR, '.home_content>div:last-child')

    btn_userout_loc = (By.CLASS_NAME, 'userout')
    btn_saveButton_loc = (By.CLASS_NAME, 'save_button')

    #通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    #打开网页
    def open(self):
        self._open(self.baseurl)

    def el_click(self, el):
        self.find_element(*el).click()

    def get_value(self, el):  #获取input文本值
        return self.find_element(*el).get_attribute('value')

    def get_text(self, el):  #获取文本
        return self.find_element(*el).text

    def click_save(self):
        self.find_element(*self.btn_saveButton_loc).click()
        sleep(2)
