#!/usr/bin/env python
#coding:utf-8

from time import sleep
from common.BasePage import BasePage
from selenium.webdriver.common.by import By

'''
Create on 2020-3-24
author:linjian
summary:工作台页面图片便签的元素对象和操作方法
'''


class WokerPic(BasePage):
    #定位器，通过元素属性定位元素对象
    headless_multiImg_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:first-child>.item_text')
    headless_img_loc = (By.CSS_SELECTOR, '.home_content.clearfix>div:nth-child(2)')
    svg_loc = (By.XPATH, '//*[@class="svg_content"]')

    tool_loc = (By.CLASS_NAME, 'work_tool')
    tool_mouse_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(1)')
    tool_img_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(5)')

    el_divs_loc = (By.CSS_SELECTOR, '.work>div')
    el_imgDIV_loc = (By.CSS_SELECTOR, '.work_image.work_element')
    el_img_loc = (By.CLASS_NAME, 'img')

    btn_imgupload_loc = (By.CLASS_NAME, 'box_img')
    btn_jianqie_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(1)')
    btn_del_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(3)')
    btn_tihuan_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(5)')
    btn_zhantie_loc = (By.CLASS_NAME, 'menu_item')

    #通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    #打开网页
    def open(self):
        self._open(self.baseurl)

    def click_imgUpload(self, el=el_imgDIV_loc):
        self.find_element(*el).click()
        sleep(1.5)

    def get_imgSrc(self):
        return self.find_element(*self.el_img_loc).get_attribute('src')
