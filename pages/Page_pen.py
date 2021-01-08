#!/usr/bin/env python
#coding:utf-8

from random import randint
from selenium.webdriver.common.action_chains import ActionChains
from common.BasePage import BasePage
from parts.tool_page import *
from parts.tool_worker import do_revoke
import os.path

'''
Create on 2021-1-6
author:linjian
summary:记号笔对象的操作方法
'''


class PenPage(BasePage):
    #定位器，通过元素属性定位元素对象
    header_loc = (By.CSS_SELECTOR, '.header.ant-layout-header')

    #左侧工具栏
    tool_loc = (By.CLASS_NAME, 'work_tool')
    tool_mouse_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(1)')
    tool_pen_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(2)')
    #记号笔工具栏
    pen_tool_loc = (By.CLASS_NAME, 'work_pen_tool')
    pen_min_loc = (By.CSS_SELECTOR, '.work_pen_tool>li:nth-child(1)')
    pen_middle_loc = (By.CSS_SELECTOR, '.work_pen_tool>li:nth-child(2)')
    pen_max_loc = (By.CSS_SELECTOR, '.work_pen_tool>li:nth-child(3)')
    pen_colorEx_loc = (By.CSS_SELECTOR, '.box.open')
    #元素相关
    el_divs_loc = (By.CSS_SELECTOR, '.work_element')
    el_text_loc = (By.CSS_SELECTOR, '.work_text.work_element')
    el_textContent_loc = (By.CSS_SELECTOR, '.work_text.work_element>.text_content')
    el_note_loc = (By.CSS_SELECTOR, '.work_note.work_element')
    el_line_loc = (By.CSS_SELECTOR, '.work_svg.work_element')
    el_lineSelected_loc = (By.CSS_SELECTOR, '.work_svg.work_element.pointer.selected')
    el_path_loc = (By.CSS_SELECTOR, '.work_svg.work_element.pointer>svg>g>path')
    el_xpath_loc = (
        By.XPATH, '//div[@class="work_svg work_element work_edit2"]/*[name()="svg"]/*[name()="g"]/*[name()="path"]')
    el_imgNote_loc = (By.CSS_SELECTOR, '.work_image.work_element')
    el_img_loc = (By.CSS_SELECTOR, '.work_image.work_element>div>.text_content>img')  #图片
    el_folder_loc = (By.CSS_SELECTOR, '.work_file.work_element')
    el_file_loc = (By.CSS_SELECTOR, '.work_wps.work_element')

    #右键菜单
    menu_paste_loc = (By.CSS_SELECTOR, '.work_menu>li:first-child')
    menu_cut_loc = (By.CSS_SELECTOR, '.text_menu>li:first-child')
    menu_copy_loc = (By.CSS_SELECTOR, '.text_menu>li:last-child')

    #通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    #打开网页
    def open(self):
        self._open(self.baseurl)

    def draw(self, num=1):
        #绘制记号笔痕迹
        width = self.driver.get_window_size()['width']
        height = self.driver.get_window_size()['height']
        poi_list = []
        for i in range(num):
            sleep(1)
            #先计算起始点
            x, y = randint(160, width - 20), randint(100, height - 200)
            end_x, end_y = randint(150, width - 20), randint(100, height - 200)
            action = ActionChains(self.driver)
            action.move_to_element_with_offset(self.find_element(*self.header_loc), x, y).click_and_hold()
            action.move_to_element_with_offset(self.find_element(*self.header_loc), end_x, end_y).release()
            action.perform()
            poi_list.append([(x, y), (end_x, end_y)])
        return poi_list

    def change_size(self, el, value, type=None):
        '''
        改变记号笔粗细
        :param el: 粗细选项按钮
        :param value: 粗细值
        :param type:操作类型，新增add
        :return:
        '''
        self.find_element(*el).click()
        sleep(1)
        size = ''
        if type == 'add':
            self.draw()
            size = self.find_element(*self.el_path_loc).value_of_css_property('stroke-width')
        else:
            size = self.find_element(*self.el_xpath_loc).value_of_css_property('stroke-width')
        print('stroke-width:{0}'.format(size), 'value:{0}'.format(value))
        assert size == value
        if type == 'add':
            do_revoke(self)
            assert bool(public_check(self, self.el_path_loc, sec=2)) == False

    def change_color(self, type=None):
        #改变记号笔颜色
        for i in range(5, 13):  #颜色按钮序号，从第5个按钮开始
            tool_color = ''
            if i < 12:
                tool_color_loc = (By.CSS_SELECTOR, '.work_pen_tool>li:nth-child({0})>div>p'.format(i))
                #工具栏选择的颜色
                color = self.find_element(*tool_color_loc).value_of_css_property('backgroundColor')
                tool_color = str(color).replace(', 1)', ')').replace('rgba', 'rgb')
                self.find_element(*tool_color_loc).click()
            else:  #更多扩展颜色
                tool_color_loc = (By.CSS_SELECTOR, '.work_pen_tool>li:nth-child({0})'.format(i))
                self.find_element(*tool_color_loc).click()
                sleep(1)
                assert bool(public_check(self, self.pen_colorEx_loc)) == True
                colorEx_loc = (By.CSS_SELECTOR, '.box.open>.bd>:nth-child(5)>li:nth-child({0})'.format(randint(1, 10)))
                #选择的颜色
                color = self.find_element(*colorEx_loc).value_of_css_property('backgroundColor')
                tool_color = str(color).replace(', 1)', ')').replace('rgba', 'rgb')
                self.find_element(*colorEx_loc).click()
            sleep(1)
            pen_color = ''
            if type == 'add':  #绘制记号笔痕迹
                self.draw()
                #记号笔痕迹颜色
                pen_color = self.find_element(*self.el_path_loc).value_of_css_property('stroke')
            else:  #记号笔痕迹颜色
                pen_color = self.find_element(*self.el_xpath_loc).value_of_css_property('stroke')
            print('tool_color:{0}'.format(tool_color), 'pen_color:{0}'.format(pen_color))
            assert tool_color == pen_color
            if type == 'add':
                do_revoke(self)
                assert bool(public_check(self, self.el_path_loc, sec=2)) == False
            sleep(1)
