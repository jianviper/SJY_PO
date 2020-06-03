#!/usr/bin/env python
#coding:utf-8

from common.BasePage import BasePage
from selenium.webdriver.common.by import By
from parts.tool_worker import left_click
import pyautogui
from time import sleep

'''
Create on 2020-3-24
author:linjian
summary:工作台页面文件夹相关的元素对象和操作方法
'''


class WorkerForlder(BasePage):
    action = None
    #定位器，通过元素属性定位元素对象
    lastProject_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:last-child>.item_text')
    svg_loc = (By.XPATH, '//*[@class="svg_content"]')

    tool_loc = (By.CLASS_NAME, 'work_tool')
    tool_mouse_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(1)')
    tool_folder_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(6)')
    tool_recovery_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(9)')

    el_divs_loc = (By.CSS_SELECTOR, '.work>div')
    el_folder_loc = (By.CSS_SELECTOR, '.work_file.work_element')
    el_fTitle_loc = (By.CLASS_NAME, 'content_title')

    btn_fjianqie_loc = (By.CSS_SELECTOR, '.task_menu>li:nth-child(1)')
    btn_fcopy_loc = (By.CSS_SELECTOR, '.task_menu>li:nth-child(2)')
    btn_del_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(3)')
    btn_fdel_loc = (By.CSS_SELECTOR, '.task_menu>li:nth-child(3)')
    btn_zhantie_loc = (By.CLASS_NAME, 'menu_item')

    #通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    #打开网页
    def open(self):
        self._open(self.baseurl)

    def input_title(self):
        self.find_element(*self.el_fTitle_loc).click()
        self.find_element(*self.el_fTitle_loc).click()
        sleep(0.5)
        pyautogui.typewrite('123', interval=0.25)
        left_click(self, 100, 100, self.svg_loc)
        # pyautogui.press('delete')
        sleep(2)
