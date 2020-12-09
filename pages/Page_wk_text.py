#!/usr/bin/env python
#coding:utf-8

from time import sleep
from common.BasePage import BasePage
from selenium.webdriver.common.by import By
from parts.tool_worker import left_click, get_text, double_click, do_revoke
from parts.tool_page import el_click
import pyautogui

'''
Create on 2020-3-24
author:linjian
summary:文本操作方法
'''


class Text(BasePage):
    #定位器，通过元素属性定位元素对象
    header_loc = (By.CSS_SELECTOR, '.header.ant-layout-header')

    tool_loc = (By.CLASS_NAME, 'work_tool')
    tool_mouse_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(1)')
    tool_text_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(5)')
    tool_textfont_loc = (By.CSS_SELECTOR, '.tool_item:first-child>img')
    tool_img_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(6)')
    tool_folder_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(8)')
    richText_tool = (By.CLASS_NAME, 'work_text_tool')  #富文本工具栏

    el_divs_loc = (By.CSS_SELECTOR, '.work_element')
    el_text_loc = (By.CSS_SELECTOR, '.work_text.work_element')
    el_textInput_loc = (By.CLASS_NAME, 'text_content')
    el_textSpan_loc = (By.CSS_SELECTOR, '.text_content>span')
    el_textFont_loc = (By.CSS_SELECTOR, '.text_content>font')
    el_imgDIV_loc = (By.CSS_SELECTOR, '.work_image.work_element')
    el_img_loc = (By.CSS_SELECTOR, '.work_image.work_element>div>.text_content>img')
    el_folder_loc = (By.CSS_SELECTOR, '.work_file.work_element')

    menu_cut_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(1)')
    menu_copy_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(2)')
    menu_del_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(3)')
    menu_paste_loc = (By.CLASS_NAME, 'menu_item')

    rich_fontFamily_loc = (By.CSS_SELECTOR, '.work_text_tool>div:nth-child(1)')
    rich_fontSize_loc = (By.CSS_SELECTOR, '.work_text_tool>div:nth-child(2)')
    rich_B_loc = (By.CSS_SELECTOR, '.work_text_tool>div:nth-child(3)')
    rich_italic_loc = (By.CSS_SELECTOR, '.work_text_tool>div:nth-child(4)')
    rich_underline_loc = (By.CSS_SELECTOR, '.work_text_tool>div:nth-child(5)')
    rich_fontColor_loc = (By.CSS_SELECTOR, '.work_text_tool>div:nth-child(6)')
    rich_leftA_loc = (By.CSS_SELECTOR, '.work_text_tool>div:nth-child(7)')
    rich_centerA_loc = (By.CSS_SELECTOR, '.work_text_tool>div:nth-child(8)')
    rich_rightA_loc = (By.CSS_SELECTOR, '.work_text_tool>div:nth-child(9)')
    rich_sortDisorder_loc = (By.CSS_SELECTOR, '.work_text_tool>div:nth-child(10)')
    rich_sortOrder_loc = (By.CSS_SELECTOR, '.work_text_tool>div:nth-child(11)')

    #通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    #打开网页
    def open(self):
        self._open(self.baseurl)

    def input_text2(self, text):
        if len(self.find_elements(*self.el_text_loc)) > 0:
            for e in self.find_elements(*self.el_text_loc):
                e.click()
                sleep(1)
                pyautogui.press('shiftleft')
                pyautogui.typewrite(text, interval=0.2)
                sleep(0.5)
            left_click(self, 50, -80, self.tool_mouse_loc)
            sleep(1)

    def text_bgColor(self, cid, textContent):
        '''
        设置文本便签背景色,判断颜色设置是否正确
        :param cid: 选项编号
        :param textContent:文本便签内的内容
        :return:
        '''
        color_item = (By.CSS_SELECTOR, '.color_item.color_{0}'.format(cid))
        rbc = self.find_element(*color_item).value_of_css_property('background-color')
        self.find_element(*color_item).click()
        sleep(1)
        text = get_text(self, self.el_text_loc)
        print(text, '\r\n', textContent)
        assert text == textContent
        bc = self.find_element(*self.el_text_loc).value_of_css_property('background-color')
        if cid == 1:
            rbc = 'rgba(255, 255, 255, 1)'
        # print(rbc, '===', bc)
        assert rbc == bc

    def check_richTextTool(self):
        #检查富文本工具栏
        from selenium.webdriver import ActionChains
        action = ActionChains(self.driver)
        for el in self.find_elements(*self.el_text_loc):
            action.double_click(el).perform()
            sleep(2)
            assert bool(self.find_element(*self.richText_tool)) == True

    def check_posi(self):
        #双击处于超出当前屏幕的文本便签
        from selenium.webdriver import ActionChains
        action = ActionChains(self.driver)
        for el in self.find_elements(*self.el_text_loc):
            if el.text == 'position':
                action.double_click(el).perform()
                sleep(2)
                assert bool(self.find_element(*self.richText_tool)) == True
                left_click(self, 100, 100, self.header_loc)

    def check_rich_style(self, richType, style_name, style_text):
        '''
        富文本设置检查。（加粗，斜体，下划线）
        :param richType: 富文本类型
        :param style_name: 样式名称
        :param style_text: 样式值
        :return:
        '''
        double_click(self, self.el_text_loc)
        double_click(self, self.el_text_loc)
        #富文本
        el_click(self, richType)
        left_click(self, 100, 100, self.header_loc)
        style = self.find_element(*self.el_textSpan_loc).value_of_css_property(style_name)
        print('style_name:{0}'.format(style))
        assert style == style_text
        do_revoke(self)
        print(self.find_element(*self.el_textSpan_loc, waitsec=3))
        assert self.find_element(*self.el_textSpan_loc, waitsec=3) == False

    def check_rich_font(self, richType):
        '''
        富文本设置检查。（字体，字号）
        :param richType: 富文本类型
        :return:
        '''
        font_item = (By.CSS_SELECTOR, '.item_select>div')
        selector_str = '.item_select>div:nth-child({0})'
        double_click(self, self.el_text_loc)
        double_click(self, self.el_text_loc)
        el_click(self, richType)  #点击富文本-字体或字号或颜色设置按钮
        if richType == self.rich_fontColor_loc:
            font_item = (By.CSS_SELECTOR, '.item_menu>div')
            selector_str = '.item_menu>div:nth-child({0})'
        item_length = len(self.find_elements(*font_item))  #获取字体或字号或颜色数量
        left_click(self, 100, 100, self.header_loc)
        for i in range(1, item_length + 1):
            double_click(self, self.el_text_loc)
            double_click(self, self.el_text_loc)
            el_click(self, richType)  #点击富文本-字体或字号或颜色设置按钮
            #点击选择
            el_click(self, (By.CSS_SELECTOR, selector_str.format(i)))
            left_click(self, 100, 100, self.header_loc)  #点画布同步
            if richType == self.rich_fontFamily_loc:  #字体
                font_name = self.find_element(*self.el_textSpan_loc).value_of_css_property('fontFamily')
                print('font_name:{0}'.format(font_name))
                if i == 1:
                    assert font_name == '微软雅黑'
                elif i == 2:
                    assert font_name == 'siyuanheiti'
                elif i == 3:
                    assert font_name == 'siyuansongti'
                elif i == 4:
                    assert font_name == 'alibabapuhuiti'
                elif i == 5:
                    assert font_name == 'Asia-Bold'
                elif i == 6:
                    assert font_name == 'BarlowCondensed-Regular'
                elif i == 7:
                    assert font_name == 'Montserrat-Regular'
            elif richType == self.rich_fontSize_loc:  #字号
                font_size = self.find_element(*self.el_textSpan_loc).value_of_css_property('fontSize')
                print('font_size:{0}'.format(font_size))
                if i == 1:
                    assert font_size == '14px'
                elif i == 2:
                    assert font_size == '16px'
                elif i == 3:
                    assert font_size == '18px'
                elif i == 4:
                    assert font_size == '20px'
                elif i == 5:
                    assert font_size == '24px'
                elif i == 6:
                    assert font_size == '28px'
            elif richType == self.rich_fontColor_loc:  #字体颜色
                if i == 1:
                    assert self.find_element(*self.el_textFont_loc, waitsec=3) == False
                else:
                    font_color = self.find_element(*self.el_textFont_loc).value_of_css_property('color')
                    print('font_color:{0}'.format(font_color))
                    if i == 2:
                        assert font_color == 'rgba(114, 114, 115, 1)'
                    elif i == 3:
                        assert font_color == 'rgba(225, 21, 32, 1)'
                    elif i == 4:
                        assert font_color == 'rgba(82, 196, 26, 1)'
                    elif i == 5:
                        assert font_color == 'rgba(24, 144, 255, 1)'
                    elif i == 6:
                        assert font_color == 'rgba(250, 219, 20, 1)'

    def check_rich_align(self, alignType, alignText):
        '''
        富文本设置检查。（文本对齐方式）
        :param alignType: 对齐方式
        :param alignText: 对齐方式值
        :return:
        '''
        div_text = (By.CSS_SELECTOR, '.text_content>:first-child')
        double_click(self, self.el_text_loc)
        el_click(self, alignType)
        left_click(self, 100, 100, self.header_loc)  #点画布同步
        text_align = self.find_element(*div_text).value_of_css_property('textAlign')
        print('text_align:{0}'.format(text_align))
        assert text_align == alignText

    def check_rich_sort(self, sortType, text):
        '''
        富文本设置检查。（有序，无序）
        :param sortType:
        :param text:
        :return:
        '''
        li_text = (By.CSS_SELECTOR, '.text_content>ul>li')
        double_click(self, self.el_text_loc)
        el_click(self, sortType)
        left_click(self, 100, 100, self.header_loc)  #点画布同步
        if sortType == self.rich_sortOrder_loc:
            li_text = (By.CSS_SELECTOR, '.text_content>ol>li>span')
        assert self.find_element(*li_text).text == text
