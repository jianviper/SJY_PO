#!/usr/bin/env python
#coding:utf-8
from selenium import webdriver
import time,os

'''
Create on 2020-3-17
author:linjian
summary:设置浏览器启动参数
'''


class BrowerSet(object):
    def __init__(self, brower_option):
        # print(os.getcwd().split('\\')[-1],'****',os.getcwd())
        if os.getcwd().split('\\')[-1]=='SJY_PO':
            self.executable_path = './driver/chromedriver.exe'
        else:
            self.executable_path = '../driver/chromedriver.exe'
        self.brower_option = brower_option
        # self.mobileEmulations = 'iPhone 6 Plus'

    def set(self):
        if self.brower_option == 'chrome':
            options = webdriver.ChromeOptions()
            options.add_argument('lang=zh_CN.UTF-8')
            # options.add_argument('--headless')
            # options.add_argument('--disable-gpu')
            # mobileEmulation = {'deviceName': self.mobileEmulations}
            # options.add_experimental_option('mobileEmulation', mobileEmulation)
            return webdriver.Chrome(executable_path=self.executable_path, options=options)

# if __name__ == '__main__':
# 	BS = BrowerSet('chrome')
# 	driver = BS.set()
# 	driver.get('http://192.168.2.4:8080/')
# 	time.sleep(5)
# 	driver.close()
