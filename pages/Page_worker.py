#!/usr/bin/env python
#coding:utf-8

import pyautogui
from random import randint
from selenium.webdriver.common.action_chains import ActionChains
from common.BasePage import BasePage
from parts.tool_page import *

'''
Create on 2020-3-24
author:linjian
summary:工作台页面的元素对象和操作方法
'''


class WorkerPage(BasePage):
    action = None
    X, Y = pyautogui.size()
    #定位器，通过元素属性定位元素对象
    header_loc = (By.CSS_SELECTOR, '.header.ant-layout-header')
    lastProject_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:last-child>.item_text')
    svg_loc = (By.XPATH, '//*[@class="svg_content"]')
    loginTips_loc = (By.XPATH, '//*[@class="ant-message"]/span//span')
    msg_loc = (By.CLASS_NAME, 'message_img')
    headless_multiImg_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:first-child>.item_text')
    headless_img_loc = (By.CSS_SELECTOR, '.home_content.clearfix>div:nth-child(2)')

    tool_loc = (By.CLASS_NAME, 'work_tool')
    tool_mouse_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(1)')
    tool_pen_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(2)')
    tool_eraser_loc = (By.CSS_SELECTOR, '.menu_item.menu_line.menu_pb.menu_flex>:last-child')
    tool_text_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(4)')
    tool_textfont_loc = (By.CSS_SELECTOR, '.tool_item:first-child>img')
    tool_img_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(5)')
    tool_folder_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(6)')
    tool_recovery_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(9)')
    tool_temp_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(8)')

    el_divs_loc = (By.CSS_SELECTOR, '.work_element')
    el_textNote_loc = (By.CSS_SELECTOR, '.work_text.work_element')
    el_textContent_loc = (By.CSS_SELECTOR, '.work_text.work_element>.text_content')
    el_line_loc = (By.CLASS_NAME, 'content_path')
    el_imgDIV_loc = (By.CSS_SELECTOR, '.work_image.work_element')
    el_img_loc = (By.CSS_SELECTOR, '.work_image.work_element>div>img')  #图片
    el_folder_loc = (By.CSS_SELECTOR, '.work_file.work_element')
    el_trashEL_loc = (By.CSS_SELECTOR, '.item_list>li')
    el_linkPoint_loc = (By.CLASS_NAME, 'relation_bottom')
    el_temp_loc = (By.CSS_SELECTOR, '.content.flex_bteween>div:first-child>div:first-child')

    btn_imgupload_loc = (By.CLASS_NAME, 'box_img')
    btn_imgCut_loc = (By.CSS_SELECTOR, '.image_menu>li:nth-child(1)')
    btn_imgCopy_loc = (By.CSS_SELECTOR, '.image_menu>li:nth-child(2)')
    btn_imgDel_loc = (By.CSS_SELECTOR, '.image_menu>li:nth-child(3)')
    btn_imgReplace_loc = (By.CSS_SELECTOR, '.image_menu>li:nth-child(7)')
    btn_cut_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(1)')
    btn_fcut_loc = (By.CSS_SELECTOR, '.file_menu>li:nth-child(1)')
    btn_copy_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(2)')
    btn_fcopy_loc = (By.CSS_SELECTOR, '.file_menu>li:nth-child(2)')
    btn_del_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(3)')
    btn_fdel_loc = (By.CSS_SELECTOR, '.file_menu>li:nth-child(3)')
    btn_tihuan_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(5)')
    btn_paste_loc = (By.CSS_SELECTOR, '.work_menu>li:first-child')
    btn_useTemp_loc = (By.CSS_SELECTOR, '.content.flex_bteween>div:first-child>.sure-btn.is-plain.use-tpl')
    btn_skip_loc = (By.CLASS_NAME, 'button_skip')
    btn_revoke_loc = (By.CSS_SELECTOR, '.actionImg.backImg')
    btn_recovery_loc = (By.CSS_SELECTOR, '.actionImg.restImg')

    #通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    #打开网页
    def open(self):
        self._open(self.baseurl)

    def draw_line(self):
        x, y = randint(80, self.X - 120), randint(190, self.Y - 100)
        dragx, dragy = randint(80, self.X - 120), randint(190, self.Y - 100)
        pyautogui.moveTo(x, y)
        pyautogui.dragTo(dragx, dragy, 1.0, button='left')
        return ((x, y), (dragx, dragy))

    def draw_line1(self):
        position = self.find_element(*self.msg_loc).location
        pos_x, pos_y = position['x'], position['y']
        start_x, start_y = randint(80, pos_x), randint(70, pos_y)
        end_x, end_y = randint(80, pos_x), randint(70, pos_y)
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(self.find_element(*self.svg_loc), start_x, start_y)
        return ((start_x, start_y), (end_x, end_y))

    def do_eraser(self, coordinate):
        sx, sy = coordinate[1][0], coordinate[0][1]
        ex, ey = coordinate[0][0], coordinate[1][1]
        print(sx, sy, ex, ey)
        # self.action.click(self.find_element(*self.svg_loc)).perform()
        # pyautogui.click(sx, sy, duration=1)
        pyautogui.doubleClick(sx, sy, duration=1)
        pyautogui.dragTo(ex, ey, 2.0, button='left')

    def choose_tool(self, el):
        self.find_element(*el).click()

    def pyag_click(self, x=None, y=None, doubleClick=None):
        if x and y:
            pyautogui.click(x, y)
        elif doubleClick:
            pyautogui.doubleClick(self.X - 200, self.Y - 200)
        else:  #没有传坐标，在画布范围内点击
            pyautogui.click(self.X - 200, self.Y - 200)
        sleep(2)

    def do_revoke(self):
        sleep(1)
        self.find_element(*self.btn_revoke_loc).click()
        sleep(1)

    def do_recovery(self):
        sleep(1)
        self.find_element(*self.btn_recovery_loc).click()
        sleep(1)

    def get_textContent(self):
        return self.find_element(*self.el_textContent_loc).text
