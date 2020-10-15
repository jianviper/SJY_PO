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
    headless_multiImg_loc = (By.CSS_SELECTOR, '.home_content>:first-child>.item_text')
    headless_img_loc = (By.CSS_SELECTOR, '.home_content>div:nth-child(2)')
    svg_loc = (By.CLASS_NAME, 'svg_content')

    tool_loc = (By.CLASS_NAME, 'work_tool')
    tool_mouse_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(1)')
    tool_img_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(6)')
    tool_folder_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(7)')

    el_divs_loc = (By.CSS_SELECTOR, '.work_element')
    el_imgDIV_loc = (By.CSS_SELECTOR, '.work_image.work_element')
    # el_img_loc = (By.CLASS_NAME, 'imgContent')
    el_img_loc = (By.CSS_SELECTOR, '.work_image.work_element>div>img')
    el_folder_loc = (By.CSS_SELECTOR, '.work_file.work_element')

    btn_imgupload_loc = (By.CLASS_NAME, 'box_img')
    btn_imgCut_loc = (By.CSS_SELECTOR, '.image_menu>li:nth-child(1)')
    btn_imgCopy_loc = (By.CSS_SELECTOR, '.image_menu>li:nth-child(2)')
    btn_imgDel_loc = (By.CSS_SELECTOR, '.image_menu>li:nth-child(3)')
    btn_imgOrigin_loc = (By.CSS_SELECTOR, '.image_menu>li:nth-child(7)')
    btn_imgMOrigin_loc = (By.CSS_SELECTOR, '.image_menu>li:nth-child(9)')
    btn_imgRorate_loc = (By.CSS_SELECTOR, '.image_menu>li:nth-child(8)')
    btn_imgMRorate_loc = (By.CSS_SELECTOR, '.image_menu>li:nth-child(10)')
    btn_imgReplace_loc = (By.CSS_SELECTOR, '.image_menu>li:nth-child(9)')
    btn_imgMReplace_loc = (By.CSS_SELECTOR, '.image_menu>li:nth-child(11)')
    btn_Paste_loc = (By.CLASS_NAME, 'menu_item')

    #通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    #打开网页
    def open(self):
        self._open(self.baseurl)

    def click_imgUpload(self, el=el_imgDIV_loc):
        self.find_element(*el).click()
        sleep(1.5)

    def get_imgSrc(self):
        return self.find_element(*self.el_img_loc).get_attribute('src')
