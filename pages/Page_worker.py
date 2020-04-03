#!/usr/bin/env python
#coding:utf-8

import pyautogui
from random import randint
from selenium.webdriver.common.action_chains import ActionChains
from common.BasePage import BasePage
from parts.pageTools import *

'''
Create on 2020-3-24
author:linjian
summary:在此封装页面的公用方法
'''


class WorkerPage(BasePage):
    action = None
    X, Y = pyautogui.size()
    #定位器，通过元素属性定位元素对象
    header_loc = (By.CSS_SELECTOR, '.header.ant-layout-header')
    lastProject_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:last-child>.item_text')
    tool_pen_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(2)')
    tool_eraser_loc = (By.CSS_SELECTOR, '.menu_item.menu_line.menu_pb.menu_flex>:last-child')
    tool_text_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(4)')
    tool_img_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(5)')
    svg_loc = (By.XPATH, '//*[@class="svg_content"]')
    el_textNote_loc = (By.CSS_SELECTOR, '.work_text.work_element')
    el_textNoteContent_loc = (By.CSS_SELECTOR, '.work_text.work_element>div')
    el_line_loc = (By.CLASS_NAME, 'content_path')
    el_img_loc = (By.CSS_SELECTOR, '.work_image.work_element')
    el_uploadImg_loc = (By.CLASS_NAME, 'img')
    textTool_font_loc = (By.CSS_SELECTOR, '.tool_item:first-child>img')
    #btn_del_loc = (By.XPATH, '//*[@class="text_menu"]/*[text()="删除"]')
    btn_del_loc=(By.CSS_SELECTOR,'.text_menu>li:nth-child(1)')
    btn_imgupload_loc = (By.CLASS_NAME, 'box_img')
    loginTips_loc = (By.XPATH, '//*[@class="ant-message"]/span//span')

    #通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    #打开网页
    def open(self):
        self._open(self.baseurl)

    def create_action(self):
        self.action = ActionChains(self.driver)

    def check(self, el, text=None, islen=False):
        if text:
            return self.find_element(*el).text == text
        elif islen:
            return len(self.driver.find_elements(*el))
        else:
            return self.find_element(*el)

    def click_intoProject(self):
        self.find_element(*self.lastProject_loc).click()
        sleep(2)

    def click_svg(self):
        return self.find_element(*self.svg_loc)

    def draw_line(self):
        x, y = randint(360, self.X - 150), randint(280, self.Y - 100)
        dragx, dragy = randint(360, self.X - 150), randint(280, self.Y - 100)
        pyautogui.moveTo(x, y)
        pyautogui.dragTo(dragx, dragy, 1.0, button='left')
        return ((x, y), (dragx, dragy))

    def do_eraser(self, coordinate):
        sx, sy = coordinate[1][0], coordinate[0][1]
        ex, ey = coordinate[0][0], coordinate[1][1]
        print(sx, sy, ex, ey)
        self.action.click(self.find_element(*self.svg_loc)).perform()
        pyautogui.click(sx, sy, duration=0.8)
        pyautogui.dragTo(ex, ey, 2.0, button='left')

    def choose_tool(self, el):
        self.find_element(*el).click()

    def action_click(self, offset_x, offset_y):
        self.action.move_by_offset(offset_x, offset_y).click().perform()

    def pyag_click(self, x=None, y=None, *args):
        if x and y:
            pyautogui.click(x, y)
        else:
            pyautogui.click(self.X - 200, self.Y - 200)
        sleep(2)

    def input_textNote(self, text):
        js = '''
        document.querySelector('.work_text.work_element').style.border='5px solid red';
        document.getElementsByClassName("text_content")[0].append('{0}');'''.format(text)
        print(js)
        self.find_element(*self.el_textNote_loc).click()
        self.driver.execute_script(js)

    def del_el(self, el):
        '''删除指定元素'''
        self.action.click(self.find_element(*el))
        self.action.context_click(self.find_element(*el)).perform()
        sleep(1.0)
        self.find_element(*self.btn_del_loc).click()
        #self.action.click(self.find_element(*self.btn_del_loc)).perform()
        wait_tips(self)

    def click_imgUpload(self):
        self.find_element(*self.el_img_loc).click()
        sleep(3)
