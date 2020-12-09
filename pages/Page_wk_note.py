#!/usr/bin/env python
#coding:utf-8

from time import sleep
from common.BasePage import BasePage
from selenium.webdriver.common.by import By
from parts.fc_tool_worker import WorkerTool
from parts.fc_tool_page import PageTool
import pyautogui

'''
Create on 2020-12-05
author:linjian
summary:便签操作方法
'''


class Note(BasePage):
    #定位器，通过元素属性定位元素对象
    header_loc = (By.CSS_SELECTOR, '.header.ant-layout-header')

    tool_note_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(6)')
    note_tool_loc = (By.CLASS_NAME, 'work_note_tool')
    rich_tool_loc = (By.CLASS_NAME, 'work_text_tool')

    el_note_loc = (By.CSS_SELECTOR, '.work_note.work_element')
    el_note_box_loc = (By.CLASS_NAME, 'note_box')
    el_note_edit_loc = (By.CSS_SELECTOR, '.work_note.work_element.work_edit2')
    el_text_blur_loc = (By.CSS_SELECTOR, '.text_content.text_blur')
    el_noteInput_loc = (By.CLASS_NAME, 'text_content')
    el_content_loc = (By.CSS_SELECTOR, '.note_box>div>div')  #便签文本内容

    btn_edit_loc = (By.CLASS_NAME, 'item_t_bg')  #富文本-T（编辑）
    btn_color_loc = (By.CSS_SELECTOR, '.work_note_tool>li>.item_border>p')  #富文本-颜色
    btn_Rsize_loc = (By.CSS_SELECTOR, '.image_arrow.text_size_right_bottom')
    rich_bold_loc = (By.CSS_SELECTOR, '.work_text_tool>div:nth-child(1)')
    rich_italic_loc = (By.CSS_SELECTOR, '.work_text_tool>div:nth-child(2)')
    rich_underline_loc = (By.CSS_SELECTOR, '.work_text_tool>div:nth-child(3)')
    rich_fontColor_loc = (By.CSS_SELECTOR, '.work_text_tool>div:nth-child(4)')
    rich_color_loc = (By.CSS_SELECTOR, '.item_menu>div>p')  #字体颜色选项

    menu_cut_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(1)')
    menu_copy_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(2)')
    menu_paste_loc = (By.CSS_SELECTOR, '.work_menu>:first-child')

    #通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    #打开网页
    def open(self):
        self._open(self.baseurl)

    def change_bgColor(self):
        #改变便签背景色，判断颜色是否正确
        for i in range(len(self.find_elements(*self.btn_color_loc))):
            btn_bgColor_list = self.find_elements(*self.btn_color_loc)
            tool_Color = btn_bgColor_list[i].value_of_css_property('backgroundColor')
            btn_bgColor_list[i].click()
            sleep(1.5)
            note_bgColor = self.find_element(*self.el_note_box_loc).value_of_css_property('backgroundColor')
            print(tool_Color, '---', note_bgColor)
            assert tool_Color == note_bgColor
            self.find_element(*self.el_note_loc).click()
            sleep(1.5)

    def input(self, text):
        self.find_element(*self.el_noteInput_loc).send_keys(text)

    def check_rich_style(self, richType, style_name, style_text):
        '''
        富文本设置检查。（加粗，斜体，下划线）
        :param richType: 富文本类型
        :param style_name: 样式名称
        :param style_text: 样式值
        :return:
        '''
        wk, pg = WorkerTool(self), PageTool(self)
        pg.el_click(self.el_note_loc)
        pg.el_click(self.btn_edit_loc)
        #富文本
        pg.el_click(richType)
        wk.left_click(type='sync')
        style = self.find_element(*self.el_content_loc).value_of_css_property(style_name)
        print('style_name:{0}'.format(style))
        assert style == style_text
        wk.do_revoke()
        assert self.find_element(*self.el_content_loc, waitsec=3) == False

    def check_rich_fontColor(self):
        #修改字体颜色
        wk, pg = WorkerTool(self), PageTool(self)
        sleep(1)
        color_list = []
        for el in self.find_elements(*self.rich_color_loc):  #获取全部字体颜色
            color_list.append(el.value_of_css_property('backgroundColor'))
        pg.el_click(self.rich_fontColor_loc)
        for i in range(len(color_list)):
            pg.el_click(self.rich_fontColor_loc)
            self.find_elements(*self.rich_color_loc)[i].click()
            note_fontColor = self.find_element(*self.el_content_loc).value_of_css_property('color')
            print(color_list[i], note_fontColor)
            assert color_list[i] == note_fontColor
