#!/usr/bin/env python
#coding:utf-8
import unittest, logging
from common.get_config import get_url
from common.create_UUID import create_uuid
from pages.Page_tiyan import TiyanPage
from parts.tool_worker import *

'''
Create on 2020-6-3
author:linjian
summary:体验用户的测试用例
'''


class TiyanTest(unittest.TestCase):
    def setUp(self) -> None:
        urls = get_url()  #return [url,home_url]
        self.url, self.home_url = urls[0], urls[1]
        uuid = create_uuid()
        self.tiyan_url = self.url + '?uuid=' + str(uuid)
        self.username = '14500000050'
        self.username2 = '14500000051'
        self.password = '123456'
        self.tiyan_PO = TiyanPage(base_url=self.tiyan_url)
        self.projectName = project_name()
        self.textContent = textNote_Content()
        self.tiyan_PO.open()

    def tearDown(self) -> None:
        self.tiyan_PO.driver.quit()

    def test_tiyan_sign(self):
        '''体验，点击右上角的注册'''
        public_check(self.tiyan_PO, self.tiyan_PO.svg_loc)
        self.assertEqual('比幕鱼 - 体验', self.tiyan_PO.driver.title)
        self.tiyan_PO.click_skip()
        self.tiyan_PO.click_menuSign()
        public_check(self.tiyan_PO, self.tiyan_PO.el_codeimg_loc)
        self.assertEqual('比幕鱼 - 注册登录', self.tiyan_PO.driver.title)

    def te1st_tiyan_vAndSign(self):
        '''体验,点击邀请-去注册'''
        public_check(self.tiyan_PO, self.tiyan_PO.svg_loc)
        self.assertEqual('比幕鱼 - 体验', self.tiyan_PO.driver.title)
        self.tiyan_PO.click_skip()
        self.tiyan_PO.click_invite()  #点击邀请
        self.tiyan_PO.click_sign()  #点击“去注册”
        public_check(self.tiyan_PO, self.tiyan_PO.el_codeimg_loc)
        self.assertEqual('比幕鱼 - 注册登录', self.tiyan_PO.driver.title)

    def te1st_tiyan_jiaocheng(self):
        '''体验，教程一步一步走完'''
        public_check(self.tiyan_PO, self.tiyan_PO.svg_loc)
        self.assertEqual('比幕鱼 - 体验', self.tiyan_PO.driver.title)
        self.assertTrue(self.tiyan_PO.find_element(*self.tiyan_PO.btn_next_loc))
        self.assertTrue('点击工具栏，绘画与创建内容', self.tiyan_PO.get_title(self.tiyan_PO.el_title_loc))
        self.tiyan_PO.click_next()
        self.assertTrue('''按住空格并拖动左键，
即可拖拽与扩展白板''', self.tiyan_PO.get_title(self.tiyan_PO.el_title_loc))
        self.tiyan_PO.click_next()
        self.assertTrue('邀请好友一起高效协作吧 ~', self.tiyan_PO.get_title(self.tiyan_PO.el_title_loc))
        self.tiyan_PO.click_finish()
        self.assertFalse(self.tiyan_PO.find_element(*self.tiyan_PO.el_course_loc, waitsec=3))

    def te1st_skip(self):
        '''跳过教程'''
        public_check(self.tiyan_PO, self.tiyan_PO.svg_loc)
        self.tiyan_PO.click_skip()
        self.assertFalse(self.tiyan_PO.find_element(*self.tiyan_PO.el_course_loc, waitsec=3))


if __name__ == "__main__":
    unittest.main()
