#!/usr/bin/env python
#coding:utf-8
import unittest
from common.get_config import get_url
from pages.Page_pen import PenPage
from parts.tool_page import *
from parts.tool_worker import *

'''
Create on 2020-3-17
update on 2021-1-6
author:linjian
summary:记号笔的测试用例
'''


class PenTest(unittest.TestCase):
    linexy = []

    def setUp(self) -> None:
        urls = get_url()  #return [url,home_url]
        self.url, self.home_url = urls[0], urls[1]
        self.username = '14500000050'
        self.password = '123456'
        self.pen_PO = PenPage(base_url=self.url)
        self.projectName = project_name()
        self.pen_PO.open()

    def tearDown(self) -> None:
        public_tearDown(self.pen_PO, self.url, self.home_url, self.username, self.password)
        self.pen_PO.driver.quit()

    def test_draws(self):
        '''使用画笔连续绘制'''
        public_init(self.pen_PO, self.username, self.password, self.projectName)
        el_click(self.pen_PO, self.pen_PO.tool_pen_loc)
        lines = self.pen_PO.draw(num=5)
        print(lines)
        self.pen_PO.driver.refresh()
        sleep(2)
        #检查是否绘制成功
        self.assertEqual(5, public_check(self.pen_PO, self.pen_PO.el_line_loc, islen=True))

    def test_draw_size(self):
        '''使用不同粗细的记号笔绘制'''
        public_init(self.pen_PO, self.username, self.password, self.projectName)
        el_click(self.pen_PO, self.pen_PO.tool_pen_loc)
        el_click(self.pen_PO, self.pen_PO.header_loc)
        #最细
        self.pen_PO.change_size(self.pen_PO.pen_min_loc, '3px', 'add')
        #中
        self.pen_PO.change_size(self.pen_PO.pen_middle_loc, '5px', 'add')
        #最粗
        self.pen_PO.change_size(self.pen_PO.pen_max_loc, '7px', 'add')

    def test_draw_color(self):
        '''使用不同颜色的记号笔绘制'''
        public_init(self.pen_PO, self.username, self.password, self.projectName)
        el_click(self.pen_PO, self.pen_PO.tool_pen_loc)
        self.pen_PO.change_color(type='add')

    def test_change_size(self):
        '''修改记号笔痕迹的粗细'''
        public_init(self.pen_PO, self.username, self.password, self.projectName)
        el_click(self.pen_PO, self.pen_PO.tool_pen_loc)
        self.pen_PO.draw()  #使用记号笔绘制
        el_click(self.pen_PO, self.pen_PO.tool_mouse_loc)
        el_click(self.pen_PO, self.pen_PO.el_line_loc)
        #检查是否显示了记号笔工具
        self.assertTrue(public_check(self.pen_PO, self.pen_PO.pen_tool_loc))
        #最细
        self.pen_PO.change_size(self.pen_PO.pen_min_loc, '3px')
        #中
        self.pen_PO.change_size(self.pen_PO.pen_middle_loc, '5px')
        #最粗
        self.pen_PO.change_size(self.pen_PO.pen_max_loc, '7px')

    def test_change_color(self):
        '''修改记号笔痕迹的颜色'''
        public_init(self.pen_PO, self.username, self.password, self.projectName)
        el_click(self.pen_PO, self.pen_PO.tool_pen_loc)
        self.pen_PO.draw()
        el_click(self.pen_PO, self.pen_PO.tool_mouse_loc)
        el_click(self.pen_PO, self.pen_PO.el_line_loc)
        self.assertTrue(public_check(self.pen_PO, self.pen_PO.pen_tool_loc))
        #修改记号笔痕迹颜色
        self.pen_PO.change_color()

    def test_copy(self):
        '''记号笔痕迹复制粘贴'''
        public_init(self.pen_PO, self.username, self.password, self.projectName)
        el_click(self.pen_PO, self.pen_PO.tool_pen_loc)
        self.pen_PO.draw()
        el_click(self.pen_PO, self.pen_PO.tool_mouse_loc)
        el_click(self.pen_PO, self.pen_PO.el_line_loc)
        #右键复制-粘贴
        rightClick(self.pen_PO, el=self.pen_PO.el_xpath_loc, action=self.pen_PO.menu_copy_loc)
        rightClick(self.pen_PO, 200, 200, self.pen_PO.header_loc, self.pen_PO.menu_paste_loc)
        left_click(self.pen_PO, 80, 80, self.pen_PO.header_loc)
        self.assertTrue(public_check(self.pen_PO, self.pen_PO.el_line_loc, islen=True) == 2)
        do_revoke(self.pen_PO)
        self.assertTrue(public_check(self.pen_PO, self.pen_PO.el_line_loc, islen=True) == 1)
        do_recovery(self.pen_PO)
        self.assertTrue(public_check(self.pen_PO, self.pen_PO.el_line_loc, islen=True) == 2)

    def test_cut(self):
        '''记号笔痕迹剪切粘贴'''
        public_init(self.pen_PO, self.username, self.password, self.projectName)
        el_click(self.pen_PO, self.pen_PO.tool_pen_loc)
        self.pen_PO.draw()
        el_click(self.pen_PO, self.pen_PO.tool_mouse_loc)
        src_poi = public_getElPoi(self.pen_PO, self.pen_PO.el_line_loc)[0]
        el_click(self.pen_PO, self.pen_PO.el_line_loc)
        #右键剪切-粘贴
        rightClick(self.pen_PO, el=self.pen_PO.el_xpath_loc, action=self.pen_PO.menu_cut_loc)
        rightClick(self.pen_PO, 200, 200, self.pen_PO.header_loc, self.pen_PO.menu_paste_loc)
        left_click(self.pen_PO, 80, 80, self.pen_PO.header_loc)
        dst_poi = public_getElPoi(self.pen_PO, self.pen_PO.el_line_loc)[0]
        print(src_poi, dst_poi)
        self.assertTrue(public_check(self.pen_PO, self.pen_PO.el_line_loc, islen=True) == 1)
        self.assertTrue(dst_poi == {'x': 200, 'y': 200})
        do_revoke(self.pen_PO)
        poi = public_getElPoi(self.pen_PO, self.pen_PO.el_line_loc)[0]
        self.assertTrue(src_poi == poi)
        do_recovery(self.pen_PO)
        poi = public_getElPoi(self.pen_PO, self.pen_PO.el_line_loc)[0]
        self.assertTrue(dst_poi == poi)


if __name__ == "__main__":
    # unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(PenTest('test_cut'))
    unittest.TextTestRunner().run(suite)
