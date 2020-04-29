#!/usr/bin/env python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.brower import BrowerSet

'''
Create on 2020-3-17
author:linjian
summary:在此封装页面的公用方法
'''


class BasePage(object):
    '''
    BasePage封装所有页面都公用的方法，例如driver, url ,FindElement等
    '''

    def __init__(self, brower_option='chrome', base_url=''):
        self.baseurl = base_url
        #供选择浏览器，默认谷歌
        BS = BrowerSet(brower_option)
        self.driver = BS.set()

    #利用get打开页面，并可以扩展做一些检查
    #_open保证在使用import *时，该方法不会被导入，保证该方法为类私有的。
    def _open(self, url):
        self.driver.get(url)
        self.driver.maximize_window()

    #定义open方法，调用_open()进行打开链接
    def open(self):
        self._open(self.baseurl)

    #重写元素定位方法
    def find_element(self, *loc, waitsec=10, check=''):
        try:
            WebDriverWait(self.driver, waitsec).until(lambda driver: driver.find_element(*loc).is_displayed())
            #WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(loc))
            return self.driver.find_element(*loc)
        except:
            print(u"%s%s 页面中未找到%s元素" % (check, self, loc))

    def find_elements(self, *loc, waitsec=10,check=''):
        try:
            WebDriverWait(self.driver, waitsec).until(lambda driver: driver.find_element(*loc).is_displayed())
            #WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(*loc))
            return self.driver.find_elements(*loc)
        except:
            print(u"%s%s 页面中未找到%s元素" % (check,self, loc))

    #重写定义send_keys方法
    def send_keys(self, loc, value, clear_first=True, click_first=True):
        try:
            loc = getattr(self, "_%s" % loc)
            if click_first:
                self.find_element(*loc).click()
            if clear_first:
                self.find_element(*loc).clear()
                self.find_element(*loc).click()
        except AttributeError:
            print(u"%s 页面中未能找到 %s 元素" % (self, loc))
