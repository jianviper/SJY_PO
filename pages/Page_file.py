#!/usr/bin/env python
#coding:utf-8
from selenium.webdriver.common.by import By
from common.BasePage import BasePage
from time import sleep

'''
Create on 2020-8-25
author:linjian
summary:文件的元素对象
'''


class FilePage(BasePage):
    #定位器，通过元素属性定位元素对象
    tool_loc = (By.CLASS_NAME, 'work_tool')
    header_loc = (By.CSS_SELECTOR, '.header.ant-layout-header')
    code_image_loc = (By.CLASS_NAME, 'code_image')
    last_proTitle_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:last-child>.item_text>.item_title')
    tips_loc = (By.CSS_SELECTOR, '.ant-message>span>.ant-message-notice')

    el_divs_loc = (By.CSS_SELECTOR, '.work_element')
    el_file_loc = (By.CSS_SELECTOR, '.work_wps.work_element')
    el_line_loc = (By.CSS_SELECTOR, '.svg_line>.content_line')
    el_prePage_loc = (By.CLASS_NAME, 'prePage')
    el_forlder_loc = (By.CSS_SELECTOR, '.work_file.work_element')

    menu_text_loc = (By.CSS_SELECTOR, '.create_menu>li:nth-child(1)')
    menu_forlder_loc = (By.CSS_SELECTOR, '.create_menu>li:nth-child(3)')

    btn_cut_loc = (By.CSS_SELECTOR, '.wps_menu>li:nth-child(1)')
    btn_copy_loc = (By.CSS_SELECTOR, '.wps_menu>li:nth-child(2)')
    btn_del_loc = (By.CSS_SELECTOR, '.wps_menu>li:nth-child(3)')
    btn_paste_loc = (By.CSS_SELECTOR, '.work_menu>li:first-child')
    btn_userout_loc = (By.CLASS_NAME, 'userout')
    btn_relright_loc = (By.CLASS_NAME, 'relation_right')
    btn_relbtm_loc = (By.CLASS_NAME, 'relation_bottom')
    btn_fileclose_loc = (By.CSS_SELECTOR, '.buttonItem.closeBtn')

    #通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    #打开网页
    def open(self):
        self._open(self.baseurl)

    def el_click(self, el):
        self.find_element(*el).click()

    def get_text(self, el):
        #返回元素内文本
        if self.find_element(*el):
            return self.find_element(*el).text
