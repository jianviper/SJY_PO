#!/usr/bin/env python
#coding:utf-8
import unittest
from time import strftime, localtime
from pages.Page_worker import WorkerPage
from parts.pageTools import *

'''
Create on 2020-4-7
author:linjian
summary:图片便签的测试用例(无上传图片功能)
'''


class ImgNoteTest(unittest.TestCase):
    def setUp(self) -> None:
        url = 'https://app.bimuyu.tech/login'
        #url = 'http://test.bimuyu.tech/login'
        self.home_url = 'https://app.bimuyu.tech/home'
        self.username = '14500000050'
        self.password = '123456'
        self.picPO = WorkerPage(base_url=url)
        self._nowtime = strftime("%Y-%m-%d %H:%M:%S", localtime())
        self.projectName = '自动化测试项目-{0}'.format(self._nowtime)
        self.textContent = '自动化测试文本-{0}'.format(self._nowtime)
        self.picPO.open()

    def tearDown(self) -> None:
        self.picPO.driver.get(self.home_url)
        if self.picPO.check((By.CLASS_NAME, 'item_text'), islen=True) > 2:
            public_delProject(self.picPO, self.home_url)
        self.picPO.driver.quit()

    def test_multiDel(self):
        '''多选删除/恢复'''
        public_login(self.picPO, self.username, self.password)
        self.picPO.click_intoProject(self.picPO.imgTest_loc)
        self.picPO.selection(self.picPO.el_imgDIV_loc)
        self.picPO.rightClick_action(el=self.picPO.el_imgDIV_loc, actionEL=self.picPO.btn_del_loc)
        #是否删除成功
        self.assertFalse(self.picPO.check(self.picPO.el_imgDIV_loc))
        self.picPO.click_trash()
        self.picPO.recovery()
        #检查恢复是否成功
        self.assertTrue(self.picPO.check(self.picPO.el_imgDIV_loc, islen=True) == 2)
        sleep(3)


if __name__ == '__main__':
    suit = unittest.TestSuite()
    # suit.addTest(ImgNoteTest('test_multiDel'))
    loader=unittest.TestLoader()
    class_test=loader.loadTestsFromTestCase(ImgNoteTest)
    suit.addTest(class_test)
    unittest.TextTestRunner().run(suit)
