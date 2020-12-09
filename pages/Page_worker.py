#!/usr/bin/env python
#coding:utf-8

import pyautogui
from random import randint
from selenium.webdriver.common.action_chains import ActionChains
from common.BasePage import BasePage
from parts.tool_page import *
import os.path

'''
Create on 2020-3-24
author:linjian
summary:工作台页面的元素对象和操作方法
'''


class WorkerPage(BasePage):
    X, Y = pyautogui.size()
    #定位器，通过元素属性定位元素对象
    header_loc = (By.CSS_SELECTOR, '.header.ant-layout-header')
    lastProject_loc = (By.CSS_SELECTOR, '.home_content>:last-child>.item_text')
    loginTips_loc = (By.XPATH, '//*[@class="ant-message"]/span//span')
    msg_loc = (By.CLASS_NAME, 'message_img')
    headless_multiImg_loc = (By.CSS_SELECTOR, '.home_content>:first-child>.item_text')
    headless_img_loc = (By.CSS_SELECTOR, '.home_content>div:nth-child(2)')
    code_image_loc = (By.CLASS_NAME, 'code_image')
    tip_page_export_loc = (By.CLASS_NAME, 'occlusion_loading')
    tip_select_export_loc = (By.CLASS_NAME, 'export_occlusion')

    #左侧工具栏
    tool_loc = (By.CLASS_NAME, 'work_tool')
    tool_mouse_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(1)')
    tool_pen_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(2)')
    tool_eraser_loc = (By.CSS_SELECTOR, '.menu_item.menu_line.menu_pb.menu_flex>:last-child')
    tool_text_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(5)')
    tool_img_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(6)')
    tool_folder_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(8)')
    tool_recovery_loc = (By.CSS_SELECTOR, '.actionBox>div:last-child')
    tool_temp_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(10)')
    #元素相关
    el_divs_loc = (By.CSS_SELECTOR, '.work_element')
    el_text_loc = (By.CSS_SELECTOR, '.work_text.work_element')
    el_textContent_loc = (By.CSS_SELECTOR, '.work_text.work_element>.text_content')
    el_note_loc = (By.CSS_SELECTOR, '.work_note.work_element')
    el_drawPath_loc = (By.CLASS_NAME, 'content_path')
    el_imgNote_loc = (By.CSS_SELECTOR, '.work_image.work_element')
    el_img_loc = (By.CSS_SELECTOR, '.work_image.work_element>div>.text_content>img')  #图片
    el_imgText_loc = (By.CSS_SELECTOR, '.work_image.work_element>div>.picTitle')
    el_folder_loc = (By.CSS_SELECTOR, '.work_file.work_element')
    el_trashEL_loc = (By.CSS_SELECTOR, '.item_list>li')
    el_temp_loc = (By.CSS_SELECTOR, '.content.flex_bteween>div:first-child>div:first-child')
    el_shareUrl_loc = (By.ID, 'shareUrl')
    el_file_loc = (By.CSS_SELECTOR, '.work_wps.work_element')
    el_relline_loc = (By.CSS_SELECTOR, '.svg_line>.content_line')
    el_line_loc = '.svg_line>.content_line'
    #右键菜单
    menu_tUp_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(4)')
    menu_export_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(5)')
    menu_tDown_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(5)')
    menu_fUp_loc = (By.CSS_SELECTOR, '.file_menu>li:nth-child(4)')
    menu_fDown_loc = (By.CSS_SELECTOR, '.file_menu>li:nth-child(5)')
    menu_wUp_loc = (By.CSS_SELECTOR, '.wps_menu>li:nth-child(4)')
    menu_wDown_loc = (By.CSS_SELECTOR, '.wps_menu>li:nth-child(5)')
    menu_imgUp_loc = (By.CSS_SELECTOR, '.image_menu>li:nth-child(4)')
    menu_imgDown_loc = (By.CSS_SELECTOR, '.image_menu>li:nth-child(5)')
    menu_imgupload_loc = (By.CLASS_NAME, 'box_img')
    menu_imgCut_loc = (By.CSS_SELECTOR, '.image_menu>li:nth-child(1)')
    menu_imgCopy_loc = (By.CSS_SELECTOR, '.image_menu>li:nth-child(2)')
    menu_imgDel_loc = (By.CSS_SELECTOR, '.image_menu>li:nth-child(3)')
    menu_imgReplace_loc = (By.CSS_SELECTOR, '.image_menu>li:nth-child(9)')
    menu_cut_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(1)')
    menu_fcut_loc = (By.CSS_SELECTOR, '.file_menu>li:nth-child(1)')
    menu_copy_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(2)')
    menu_fcopy_loc = (By.CSS_SELECTOR, '.file_menu>li:nth-child(2)')
    menu_del_loc = (By.CSS_SELECTOR, '.text_menu>li:nth-child(3)')
    menu_fdel_loc = (By.CSS_SELECTOR, '.file_menu>li:nth-child(3)')
    menu_paste_loc = (By.CSS_SELECTOR, '.work_menu>li:first-child')
    #拉出关联线的菜单
    menu_text_loc = (By.CSS_SELECTOR, '.create_menu>li:nth-child(1)')
    menu_forlder_loc = (By.CSS_SELECTOR, '.create_menu>li:nth-child(3)')
    #按钮相关
    btn_useTemp_loc = (By.CSS_SELECTOR, '.content.flex_bteween>div:first-child>.sure-btn.is-plain.use-tpl')
    btn_skip_loc = (By.CLASS_NAME, 'button_skip')
    btn_export_loc = (By.CLASS_NAME, 'export')
    btn_page_export_loc = (By.CSS_SELECTOR, '.export_menu>li:last-child')
    btn_revoke_loc = (By.CSS_SELECTOR, '.actionBox>div:first-child')
    btn_recovery_loc = (By.CSS_SELECTOR, '.actionBox>div:last-child')
    btn_userout_loc = (By.CLASS_NAME, 'userout')
    btn_relB_loc = (By.CLASS_NAME, 'relation_bottom')
    btn_relR_loc = (By.CLASS_NAME, 'relation_right')

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

    def get_textContent(self) -> str:
        return self.find_element(*self.el_textContent_loc).text

    def check_file(self, name) -> bool:
        '''检查文件是否存在'''
        sleep(3)
        path = r'C:\Users\SJY-J\Downloads\{0}.png'.format(name)
        print('path:{0}'.format(path))
        return os.path.exists(path)

    def page_export(self):
        #本页导出
        action = ActionChains(self.driver)
        action.move_to_element(self.find_element(*self.btn_export_loc)).perform()
        sleep(1)
        print('export:', self.find_element(*self.btn_page_export_loc))
        # action.click(self.find_element(*self.btn_page_export_loc)).perform()
        self.find_element(*self.btn_page_export_loc).click()
