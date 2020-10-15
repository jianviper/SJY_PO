#!/usr/bin/env python
#coding:utf-8

from time import sleep
from common.BasePage import BasePage
from selenium.webdriver.common.by import By
from parts.tool_worker import left_click, get_text
import pyautogui

'''
Create on 2020-3-24
author:linjian
summary:工作台页面的元素对象和操作方法
'''


class WorkerTextNote(BasePage):
    #定位器，通过元素属性定位元素对象
    lastProject_loc = (By.CSS_SELECTOR, '.home_content>:last-child>.item_text')
    header_loc = (By.CSS_SELECTOR, '.header.ant-layout-header')

    tool_loc = (By.CLASS_NAME, 'work_tool')
    tool_mouse_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(1)')
    tool_text_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(5)')
    tool_textfont_loc = (By.CSS_SELECTOR, '.tool_item:first-child>img')
    tool_img_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(6)')
    tool_folder_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(7)')
    text_tool = (By.CLASS_NAME, 'work_text_tool')  #富文本工具栏

    el_divs_loc = (By.CSS_SELECTOR, '.work_element')
    el_textNote_loc = (By.CSS_SELECTOR, '.work_text.work_element')
    el_textNoteText_loc = (By.CLASS_NAME, 'text_content')
    el_imgDIV_loc = (By.CSS_SELECTOR, '.work_image.work_element')
    el_img_loc = (By.CSS_SELECTOR, '.work_image.work_element>div>img')
    el_folder_loc = (By.CSS_SELECTOR, '.work_file.work_element')

    menu_cut_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(1)')
    menu_copy_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(2)')
    menu_del_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(3)')
    menu_paste_loc = (By.CLASS_NAME, 'menu_item')

    #通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    #打开网页
    def open(self):
        self._open(self.baseurl)

    def input_textNote(self, text):
        #文本便签利用JS进行赋值
        js = '''
        document.querySelector('.work_text.work_element').style.border='5px solid red';
        document.getElementsByClassName("text_content")[0].append('{0}');'''.format(text)
        jss = '''
        var ds=document.getElementsByClassName('text_content'); 
        for(i=0;i<ds.length;i++){
            ds[i].parentNode.style.border='3px solid red';
            ds[i].append("{0}");
        }
        '''.format(text)
        self.driver.execute_script(jss)
        if len(self.find_elements(*self.el_textNote_loc)) > 0:
            for e in self.find_elements(*self.el_textNote_loc):
                e.click()
                sleep(1)
                left_click(self, 50, -80, self.tool_mouse_loc)

    def input_textNote2(self, text):
        if len(self.find_elements(*self.el_textNote_loc)) > 0:
            for e in self.find_elements(*self.el_textNote_loc):
                e.click()
                sleep(1)
                pyautogui.press('shiftleft')
                pyautogui.typewrite(text, interval=0.2)
                sleep(0.5)
            left_click(self, 50, -80, self.tool_mouse_loc)
            sleep(1)

    def set_color(self, el):
        bc = self.find_element(*el).value_of_css_property('background-color')
        self.find_element(*el).click()
        print('r_bc:{0}'.format(bc))
        return bc

    def getc(self, cid, textContent):
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
        text = get_text(self, self.el_textNote_loc)
        assert text == textContent
        bc = self.find_element(*self.el_textNote_loc).value_of_css_property('background-color')
        if cid == 1:
            rbc = 'rgba(255, 255, 255, 1)'
        # print(rbc, '===', bc)
        assert rbc == bc
