#!/usr/bin/env python
#coding:utf-8
from time import sleep
from selenium.webdriver.common.by import By


def wait_tips(pageObject):
    loginTips_loc = (By.XPATH, '//*[@class="ant-message"]/span//span')
    i = 0
    print('parts_jinru')
    while not pageObject.find_element(*loginTips_loc):
        print('wait:{0}'.format(i))
        if i > 7:
            break
        i += 1
        sleep(1.5)