#!/usr/bin/env python
#coding:utf-8
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from common.BasePage import BasePage
from parts.tool_page import wait_tips
from time import sleep

'''
Create on 2020-3-18
author:linjian
summary:模版的元素对象
'''


class TemplatePage(BasePage):
    #定位器，通过元素属性定位元素对象
    header_loc = (By.CSS_SELECTOR, '.header.ant-layout-header')
    tool_loc = (By.CLASS_NAME, 'work_tool')
    tool_temp_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(9)')

    el_tempImg_loc = (By.CSS_SELECTOR, '.content.flex_bteween>div:first-child>div:first-child')
    el_divs_loc = (By.CSS_SELECTOR, '.work_element')
    el_searchInput_loc = (By.CSS_SELECTOR, '.searchInput.form-line')
    el_resultName_loc = (By.CLASS_NAME, 'name')
    el_secondtext_loc = (By.CLASS_NAME, 'secondtext')
    el_tempName_loc = (By.CSS_SELECTOR, '.no-input.data-name>.searchInput.form-line')
    el_job_loc = (By.CSS_SELECTOR, '.no-input.data-job>.searchInput.form-line')
    el_notfind_loc = (By.CSS_SELECTOR, '.helpOut.pointer_cursor.flex_bteween')
    el_warnTitle_loc = (By.CLASS_NAME, 'warn_title')

    btn_useTemp_loc = (By.CSS_SELECTOR, '.content.flex_bteween>div:first-child>.sure-btn.is-plain.use-tpl')
    btn_search_loc = (By.CLASS_NAME, 'iconsearch')
    btn_submit_loc = (By.CSS_SELECTOR, '.sure-btn.is-plain.submit-info')
    btn_submit2_loc = (By.CSS_SELECTOR, '.sure-btn.submit-info')

    lastProjectName_loc = (By.CSS_SELECTOR, '.home_content>:last-child>.item_text>.item_title')

    #通过继承覆盖（Overriding）方法：如果子类和父类的方法名相同，优先用子类自己的方法。
    #打开网页
    def open(self):
        self._open(self.baseurl)

    def choose_template(self):
        self.find_element(*self.tool_temp_loc).click()
        sleep(2)

    def add_temp(self):
        self.choose_template()
        self.do_search('SWOT')
        action = ActionChains(self.driver)
        action.move_to_element(self.find_element(*self.el_tempImg_loc)).perform()
        sleep(1)
        self.find_element(*self.btn_useTemp_loc).click()
        sleep(1.5)
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(self.find_element(*self.header_loc), 200, 200).click().perform()
        sleep(1)

    def do_search(self, text):
        self.find_element(*self.el_searchInput_loc).send_keys(text)
        # self.find_element(*self.btn_search_loc).click()
        action = ActionChains(self.driver)
        action.click(self.find_element(*self.btn_search_loc)).perform()
        sleep(3)

    def submit_myTemp(self, name, job, sb=1):
        el = self.btn_submit_loc
        self.find_element(*self.el_tempName_loc).send_keys(name)
        self.find_element(*self.el_job_loc).send_keys(job)
        if sb == 2: el = self.btn_submit2_loc
        self.find_element(*el).click()
        wait_tips(self)

    def click_notfind(self):
        self.find_element(*self.el_notfind_loc).click()
        sleep(2)

    def click_submit(self):
        self.find_element(*self.btn_submit_loc).click()
        sleep(1)
