#!/usr/bin/env python
#coding:utf-8
from selenium import webdriver
import os

'''
Create on 2020-3-17
author:linjian
summary:设置浏览器启动参数
'''


class BrowerSet(object):
    def __init__(self, brower_name):
        self.brower_name = brower_name
        # print(os.getcwd().split('\\')[-1],'****',os.getcwd())
        if brower_name == 'chrome':
            brower_name = 'chromedriver'
        if os.getcwd().split('\\')[-1] == 'SJY_PO':
            self.path = './driver/{0}.exe'.format(brower_name)
        else:
            self.path = '../driver/{0}.exe'.format(brower_name)
        # self.mobileEmulations = 'iPhone 6 Plus'

    def set(self):
        if self.brower_name == 'chrome':
            options = webdriver.ChromeOptions()
            store_path = r'C:\Users\SJY-J\Downloads'
            prefs = {'download.default_directory': store_path,
                     'profile.default_content_settings.popups': 0}
            options.add_experimental_option('prefs', prefs)
            options.add_argument('lang=zh_CN.UTF-8')
            options.add_argument('--headless')  #无界面浏览器
            options.add_argument('--disable-gpu')
            options.add_argument("--window-size=1920,1080")  #设置浏览器宽高
            options.add_experimental_option('excludeSwitches', ['enable-automation'])  #避免检测
            # options.add_argument('blink-settings=imagesEnabled=false')
            # mobileEmulation = {'deviceName': self.mobileEmulations}
            # options.add_experimental_option('mobileEmulation', mobileEmulation)
            return webdriver.Chrome(executable_path=self.path, options=options)
        elif self.brower_name == 'edge':
            return webdriver.Edge(self.path)
        elif self.brower_name == 'ie':
            return webdriver.Ie(executable_path=self.path)

# if __name__ == '__main__':
# 	BS = BrowerSet('chrome')
# 	driver = BS.set()
# 	driver.get('http://192.168.2.4:8080/')
# 	time.sleep(5)
# 	driver.close()
