#!/usr/bin/env python
#coding:utf-8

from time import sleep
from selenium.webdriver.common.by import By

def createProject(pageObject,name):
    '''创建项目'''
    pageObject.click_createProject()
    pageObject.input_create_projectName(name)
    pageObject.click_CPSubmit()

def public_createProject(pageObject,name):
    createProject_loc = (By.CSS_SELECTOR, '.header_add.ant-btn.ant-btn-default')
    projectName_loc = (By.CLASS_NAME, 'ant-input')
    CPSubmitButton_loc = (By.CSS_SELECTOR, '.footer_submit.ant-btn.ant-btn-default')

    pageObject.find_element(*createProject_loc).click()
    pageObject.find_element(*projectName_loc).send_keys(name)
    pageObject.find_element(*CPSubmitButton_loc).click()
    sleep(1)

def public_delProject(pageObject):
    lastProjectMenu_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:last-child>.item_set>img')
    delMenuButton_loc = (By.CSS_SELECTOR, '.home_content.clearfix>:last-child>ul>:last-child')
    delProjectName_loc = (By.CSS_SELECTOR, '.header_subtitle>span')
    inputProjectName_loc = (By.CSS_SELECTOR, '.form_item>input[type=text]')
    delSubmitButton_loc = (By.CSS_SELECTOR, '.footer_submit.ant-btn.ant-btn-default')
    Tips_loc = (By.XPATH, '//*[@class="ant-message"]/span//span')

    pageObject.find_element(*lastProjectMenu_loc).click()
    pageObject.find_element(*delMenuButton_loc).click()
    pageObject.find_element(*inputProjectName_loc).send_keys(pageObject.find_element(*delProjectName_loc).text)
    pageObject.find_element(*delSubmitButton_loc).click()

    return pageObject.find_element(*Tips_loc).text