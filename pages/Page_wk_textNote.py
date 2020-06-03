#!/usr/bin/env python
#coding:utf-8

from time import sleep
from common.BasePage import BasePage
from selenium.webdriver.common.by import By
from parts.tool_worker import left_click

'''
Create on 2020-3-24
author:linjian
summary:工作台页面的元素对象和操作方法
'''


class WorkerTextNote(BasePage):
    #定位器，通过元素属性定位元素对象
    lastProject_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:last-child>.item_text')
    svg_loc = (By.XPATH, '//*[@class="svg_content"]')

    tool_loc = (By.CLASS_NAME, 'work_tool')
    tool_mouse_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(1)')
    tool_text_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(4)')
    tool_textfont_loc = (By.CSS_SELECTOR, '.tool_item:first-child>img')
    tool_img_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(5)')
    tool_folder_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(6)')

    el_divs_loc = (By.CSS_SELECTOR, '.work>div')
    el_textNote_loc = (By.CSS_SELECTOR, '.work_text.work_element')
    el_textNoteText_loc = (By.CLASS_NAME, 'text_content')
    el_imgDIV_loc = (By.CSS_SELECTOR, '.work_image.work_element')
    el_img_loc = (By.CLASS_NAME, 'img')
    el_folder_loc = (By.CSS_SELECTOR, '.work_file.work_element')

    btn_jianqie_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(1)')
    btn_copy_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(2)')
    btn_del_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(3)')
    btn_zhantie_loc = (By.CLASS_NAME, 'menu_item')

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
            ds[i].append("%s");
        }
        ''' % text
        self.driver.execute_script(jss)
        if len(self.find_elements(*self.el_textNote_loc)) > 0:
            for e in self.find_elements(*self.el_textNote_loc):
                e.click()
                sleep(1)
                left_click(self, 50, -80, self.tool_mouse_loc)
