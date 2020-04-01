#!/usr/bin/env python
#coding:utf-8
from time import sleep
from selenium.webdriver.common.by import By


def login(page, username, password, flag=0,code=0):
    '''flag是否需要登录成功，code是否用验证码登录'''
    page.open()
    if code==0:
        page.choose_pwLogin()
    page.input_username(username)
    page.input_password(password)
    page.click_submit()
    if flag == 1:
        i = 0
        while page.driver.title != r'比幕鱼 - 项目列表':
            if i > 5:
                break
            i += 1
            sleep(2)

def publicLogin(pageObject,username,password):
    '''公用登录方法'''
    pwLogin_loc = (By.XPATH, '//*[@class="login_content"]//span')
    username_loc = (By.XPATH, '//*[@class="form_item"][1]/input')
    password_loc = (By.XPATH, '//*[@class="form_item"][2]/input')
    loginSubmit_loc = (By.CLASS_NAME, 'item_submit')

    pageObject.open()
    sleep(2)
    pageObject.find_element(*pwLogin_loc).click()
    pageObject.find_element(*username_loc).send_keys(username)
    pageObject.find_element(*password_loc).send_keys(password)
    pageObject.find_element(*loginSubmit_loc).click()
    i = 0
    while pageObject.driver.title != r'比幕鱼 - 项目列表':
        if i > 5:
            break
        i += 1
        sleep(2)