#!/usr/bin/env python
#coding:utf-8
from selenium.webdriver.common.by import By
from common.BasePage import BasePage
from time import sleep

'''
Create on 2020-3-18
author:linjian
summary:Home页的元素对象
'''


class HomePage(BasePage):
    #定位器，通过元素属性定位元素对象
    delProjectName_loc = (By.CSS_SELECTOR, '.header_subtitle>span')  #删除要确认的名称
    Tips_loc = (By.XPATH, '//*[@class="ant-message"]/span//span')
    num_project_loc = (By.CSS_SELECTOR, '.home_content.clearfix>div')  #项目数量
    firstProject_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:first-child')  #第一个项目
    win_bind_loc = (By.CLASS_NAME, 'ant-modal-body')  #
    log_content_loc = (By.CLASS_NAME, 'log_content')
    log_loc = (By.CSS_SELECTOR, '.log.log_open')
    log_title_loc = (By.CLASS_NAME, 'increase_title')

    input_proName_loc = (By.CSS_SELECTOR, '.form-line.iteminput')
    input_delName_loc = (By.CSS_SELECTOR, '.form_item>.form-line.iteminput')

    btn_help_loc = (By.CLASS_NAME, 'guideHelp')
    btn_user_loc = (By.CSS_SELECTOR, '.menu_user.mouse_hover')
    btn_createProject_loc = (By.CSS_SELECTOR, '.home_header>.sure-btn.submit-info')
    #CRD:创建，重命名，删除 按钮
    btn_CR_loc = (By.CSS_SELECTOR, '.add_footer.modal_foot>:last-child>.sure-btn.submit-info')
    btn_projectMenu_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:first-child>.item_set>img')
    btn_menu_rename_loc = (By.CSS_SELECTOR, '.item_menu>li:first-child')
    btn_del_loc = (By.CSS_SELECTOR, '.footBtn.delBtn')
    btn_delSubmit_loc = (By.CSS_SELECTOR, '.add_footer>.sure-btn.submit-info')
    btn_closeBind_loc = (By.CLASS_NAME, 'closeBtn')
    btn_log_close_loc = (By.CLASS_NAME, 'header_close')

    menu_user_loc = (By.CLASS_NAME, 'meny_level2')  #头像点击菜单
    menu_update_loc = (By.CSS_SELECTOR, '.meny_level2>li:nth-child(5)')  #点击更新日志

    firstPro_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:first-child')
    firstProMenu_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:first-child>.item_set')
    firstProName_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:first-child>.item_text>.item_title')
    lastProName_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:last-child>.item_text>.item_title')
    lastProMenu_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:last-child>.item_set')

    #通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    #打开网页
    def open(self):
        self._open(self.baseurl)

    def go_helpPage(self):
        self.find_element(*self.btn_help_loc).click()

    def go_userMenu(self):
        self.find_element(*self.btn_user_loc).click()

    def check_userMenu(self):
        return self.find_element(*self.menu_user_loc)

    def click_updateLog(self):
        self.find_element(*self.menu_update_loc).click()

    def click_createProject(self):
        #点击"新建项目"
        self.find_element(*self.btn_createProject_loc).click()

    def input_create_projectName(self, name):
        self.find_element(*self.input_proName_loc).send_keys(name)

    def click_CRDSubmit(self):
        #创建，重命名的确定按钮
        self.find_element(*self.btn_CR_loc).click()
        sleep(1)

    def get_ProjectName(self, el):
        #获取某个项目的名称
        return self.find_element(*el).text

    def click_lastProjectMenu(self):
        self.find_element(*self.lastProMenu_loc).click()

    def click_firstProjectMenu(self):
        #第一个项目的右上角menu
        from selenium.webdriver.common.action_chains import ActionChains
        action = ActionChains(self.driver)
        action.move_to_element(self.find_element(*self.firstPro_loc)).perform()
        self.find_element(*self.firstProMenu_loc).click()
        sleep(1)

    def go_del(self):  #删除白板流程
        self.click_firstProjectMenu()
        self.find_element(*self.btn_del_loc).click()
        sleep(1)
        self.input_projectName(d=True)
        self.find_element(*self.btn_delSubmit_loc).click()
        sleep(1)

    def click_renameButton(self):
        self.find_element(*self.btn_menu_rename_loc).click()

    def input_projectName(self, name='', d=None):
        '''
        输入白板名称
        :param name:白板名称
        :param d: 为True表示删除白板
        :return:
        '''
        el = self.input_proName_loc
        if name == '' and d:
            name = self.find_element(*self.delProjectName_loc).text
            el = self.input_delName_loc
        self.send_keys(el, name)

    def get_tips(self):
        return self.find_element(*self.Tips_loc).text

    def get_projectNum(self):
        '''
        返回白板数量
        :return: 白板数量
        '''
        num = self.driver.find_elements(*self.num_project_loc).__len__()
        return num

    def click_firstProject(self):
        self.find_element(*self.firstProject_loc).click()

