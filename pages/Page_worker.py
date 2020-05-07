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
    headless_multiImg_loc=(By.CSS_SELECTOR, '.home_content.clearfix>:first-child>.item_text')
    headless_img_loc=(By.CSS_SELECTOR,'.home_content.clearfix>div:nth-child(2)')

    tool_loc = (By.CLASS_NAME, 'work_tool')
    tool_mouse_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(1)')
    tool_pen_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(2)')
    tool_eraser_loc = (By.CSS_SELECTOR, '.menu_item.menu_line.menu_pb.menu_flex>:last-child')
    tool_text_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(4)')
    tool_textfont_loc = (By.CSS_SELECTOR, '.tool_item:first-child>img')
    tool_img_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(5)')
    tool_folder_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(6)')
    tool_recovery_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(9)')

    el_divs_loc = (By.CSS_SELECTOR, '.work>div')
    el_textNote_loc = (By.CSS_SELECTOR, '.work_text.work_element')
    el_textNoteText_loc = (By.CLASS_NAME, 'text_content')
    el_line_loc = (By.CLASS_NAME, 'content_path')
    el_imgDIV_loc = (By.CSS_SELECTOR, '.work_image.work_element')
    el_img_loc = (By.CLASS_NAME, 'img')
    el_folder_loc = (By.CSS_SELECTOR, '.work_file.work_element')
    el_trashEL_loc = (By.CSS_SELECTOR, '.item_list>li')

    #btn_del_loc = (By.XPATH, '//*[@class="text_menu"]/*[text()="删除"]')
    btn_imgupload_loc = (By.CLASS_NAME, 'box_img')
    btn_jianqie_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(1)')
    btn_fjianqie_loc = (By.CSS_SELECTOR, '.task_menu>li:nth-child(1)')
    btn_del_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(3)')
    btn_fdel_loc = (By.CSS_SELECTOR, '.task_menu>li:nth-child(3)')
    btn_tihuan_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(5)')
    btn_zhantie_loc = (By.CLASS_NAME, 'menu_item')

    #通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    #打开网页
    def open(self):
        self._open(self.baseurl)

    def check(self, el, text=None, islen=False):
        #根据判定需求返回不同检查结果
        if text:
            for e in self.find_elements(*el, waitsec=5, check='【check】'):
                if e.text != text:
                    return False
            return True
        elif islen:
            return len(self.find_elements(*el, waitsec=5, check='【check】'))
        else:
            return self.find_element(*el, waitsec=5, check='【check】')

    def click_intoProject(self,el=lastProject_loc):
        self.find_element(*el).click()
        sleep(2)

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

    def input_textNote(self, text):
        #文本便签利用JS进行赋值
        js = '''
        document.querySelector('.work_text.work_element').style.border='5px solid red';
        document.getElementsByClassName("text_content")[0].append('{0}');'''.format(text)
        jss = '''
        var ds=document.getElementsByClassName('text_content'); 
        for(i=0;i<ds.length;i++){
            ds[i].parentNode.style.border='5px solid red';
            ds[i].append("%s");
        }
        ''' % text
        self.driver.execute_script(jss)
        for e in self.find_elements(*self.el_textNote_loc):
            e.click()
            sleep(1)
            self.action_click(50, -80, self.tool_mouse_loc)

    def action_click(self, x=0, y=0, el=None):
        '''左键点击，可以指定元素及相对位置进行'''
        action = ActionChains(self.driver)
        if x and y and el:  #在指定元素的相对位置
            action.move_to_element_with_offset(self.find_element(*el), x, y).click().perform()
        elif x and y:  #在当前鼠标位置的相对偏移位置
            action.move_by_offset(x, y).click().perform()
        elif el:  #在指定元素上
            action.click(self.find_element(*el)).perform()
        sleep(1.5)

    def rightClick_action(self, x=0, y=0, el=None, actionEL=None):
        '''右键点击,可以指定元素及其相对位置，也可右键菜单操作'''
        action = ActionChains(self.driver)
        if x and y and el:  #在指定元素的相对位置
            action.move_to_element_with_offset(self.find_element(*el), x, y).context_click().perform()
        elif el:  #在指定元素上
            action.context_click(self.find_element(*el)).perform()
        else:  #在鼠标当前位置
            action.context_click().perform()
        sleep(1.0)
        if actionEL:
            self.find_element(*actionEL).click()
            sleep(1.5)
        if actionEL == self.btn_del_loc:
            wait_tips(self)

    def click_imgUpload(self, el=el_imgDIV_loc):
        self.find_element(*el).click()
        sleep(1.5)

    def get_imgSrc(self):
        return self.find_element(*self.el_img_loc).get_attribute('src')

    def get_selectPosition(self, el):
        #获取设置指定元素的选取范围
        x, y = [], []
        for e in self.find_elements(*el):
            x.append(e.location['x'])
            y.append(e.location['y'])
        print(x, y)
        return ((min(x) - 20, min(y) - 20), (max(x) + 20, max(y) + 20))
        # return (self.find_element(*el).location, self.find_element(*el).location_once_scrolled_into_view)

    def selection(self, el):
        '''根据需求多选元素'''
        SP = self.get_selectPosition(el)
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(self.find_element(*self.svg_loc), SP[0][0], SP[0][1])
        action.click_and_hold().move_by_offset(SP[1][0], SP[1][1]).release().perform()

    def click_trash(self):
        self.find_element(*self.tool_recovery_loc).click()

    def recovery(self):
        '''恢复删除的元素'''
        for el in self.find_elements(*self.el_trashEL_loc):
            el.click()
            sleep(0.5)
        self.find_element(*self.tool_mouse_loc).click()
