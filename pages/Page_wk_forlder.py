#!/usr/bin/env python
#coding:utf-8

from common.BasePage import BasePage
from selenium.webdriver.common.by import By
from parts.tool_worker import left_click
# import pyautogui
from time import sleep
from selenium.webdriver import ActionChains

'''
Create on 2020-3-24
author:linjian
summary:工作台页面文件夹相关的元素对象和操作方法
'''


class WorkerForlder(BasePage):
    action = None
    #定位器，通过元素属性定位元素对象
    lastProject_loc = (By.CSS_SELECTOR, '.home_content>:last-child>.item_text')
    svg_loc = (By.XPATH, '//*[@class="svg_content"]')
    tips_loc = (By.CSS_SELECTOR, '.ant-notification-notice.ant-notification-notice-closable')
    right_menu_loc = (By.CLASS_NAME, 'task_menu')
    header_loc = (By.CSS_SELECTOR, '.header.ant-layout-header')

    tool_loc = (By.CLASS_NAME, 'work_tool')
    tool_mouse_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(1)')
    tool_folder_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(6)')
    tool_recovery_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(9)')

    el_divs_loc = (By.CSS_SELECTOR, '.work_element')
    el_textNote_loc = (By.CSS_SELECTOR, '.work_text.work_element')
    el_folder_loc = (By.CSS_SELECTOR, '.work_file.work_element')
    el_fTitle_loc = (By.CLASS_NAME, 'content_title2')
    el_titleInput_loc = (By.CSS_SELECTOR, '.content_title.ant-input')
    el_folderImg_loc = (By.CSS_SELECTOR, '.file_content>div>img')
    el_line_loc = '//*[@class="work_svg"]/*[name()="svg"][2]/*[name()="line"]'
    el_line2_loc = '.svg_line>.content_line'

    btn_bread_loc = (By.CSS_SELECTOR, '.header_crumbs.ant-breadcrumb>span:first-child>span:first-child')
    btn_fjianqie_loc = (By.CSS_SELECTOR, '.file_menu>li:nth-child(1)')
    btn_fcopy_loc = (By.CSS_SELECTOR, '.file_menu>li:nth-child(2)')
    btn_del_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(3)')
    btn_fdel_loc = (By.CSS_SELECTOR, '.file_menu>li:nth-child(3)')
    btn_paste_loc = (By.CLASS_NAME, 'menu_item')
    btn_color_loc = (By.CSS_SELECTOR, '.flex_row_around.colormenu>span:nth-child(2)')
    btn_relbtm_loc = (By.CLASS_NAME, 'relation_bottom')

    #通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    #打开网页
    def open(self):
        self._open(self.baseurl)

    def input_title(self, title):
        from selenium.webdriver import ActionChains
        action = ActionChains(self.driver)
        action.double_click(self.find_element(*self.el_fTitle_loc)).perform()
        # self.find_element(*self.el_fTitle_loc).click()
        sleep(0.5)
        self.find_element(*self.el_titleInput_loc).click()
        self.find_element(*self.el_titleInput_loc).clear()
        sleep(0.5)
        # pyautogui.typewrite('123', interval=0.25)
        self.find_element(*self.el_titleInput_loc).send_keys(title)
        left_click(self, 50, 100, self.header_loc)
        # pyautogui.press('delete')
        sleep(2)

    def get_title(self):
        return self.find_element(*self.el_fTitle_loc).text

    def enter(self, index=0):  #进入文件夹
        action = ActionChains(self.driver)
        action.double_click(self.find_elements(*self.el_folder_loc)[index]).perform()
        sleep(2)
