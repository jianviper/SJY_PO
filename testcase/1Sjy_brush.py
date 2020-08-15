#!/usr/bin/env python
#coding:utf-8
import unittest
from common.get_config import get_url
from pages.Page_worker import WorkerPage
from parts.tool_page import *
from parts.tool_worker import left_click

'''
Create on 2020-3-17
author:linjian
summary:画笔和橡皮擦的测试用例
'''


class WorkerTest(unittest.TestCase):
    linexy = []

    def setUp(self) -> None:
        urls = get_url()  #return [url,home_url]
        self.url, self.home_url = urls[0], urls[1]
        self.username = '14500000050'
        self.password = '123456'
        self.brush_PO = WorkerPage(base_url=self.url)
        self.projectName = project_name()
        self.lineNum = 5
        self.brush_PO.open()

    def tearDown(self) -> None:
        # public_tearDown(self.brush_PO, self.url, self.home_url, self.username, self.password)
        self.brush_PO.driver.quit()

    def test_draw(self):
        '''使用画笔绘制'''
        public_init(self.brush_PO, self.username, self.password, self.projectName)
        self.brush_PO.choose_tool(self.brush_PO.tool_pen_loc)
        n = i = self.lineNum

        left_click(self.brush_PO, 50, 100, self.brush_PO.header_loc)
        while i > 0:  #绘制多条痕迹
            self.linexy.append(self.brush_PO.draw_line())
            i -= 1
            sleep(1)
        print(self.projectName, '\r\n', self.linexy)
        self.brush_PO.driver.refresh()
        sleep(2)
        #检查是否绘制成功
        self.assertIs(self.lineNum, public_check(self.brush_PO, self.brush_PO.el_line_loc, islen=True))

    def test_eraser(self):
        '''使用橡皮擦'''
        public_init(self.brush_PO, self.username, self.password, self.projectName)
        self.brush_PO.choose_tool(self.brush_PO.tool_pen_loc)
        left_click(self.brush_PO, 150, 100, self.brush_PO.svg_loc)
        n = i = self.lineNum
        while i > 0:  #绘制多条痕迹
            self.linexy.append(self.brush_PO.draw_line())
            i -= 1
            sleep(0.6)
        #检查是否绘制成功
        self.assertIs(self.lineNum, public_check(self.brush_PO, self.brush_PO.el_line_loc, islen=True))
        self.brush_PO.choose_tool(self.brush_PO.tool_pen_loc)
        self.brush_PO.choose_tool(self.brush_PO.tool_eraser_loc)
        print(self.linexy[0])
        self.brush_PO.do_eraser(self.linexy[0])  #擦除第一根痕迹
        #是否擦除成功
        self.assertLess(public_check(self.brush_PO, self.brush_PO.el_line_loc, islen=True), self.lineNum)
        public_delProject(self.brush_PO, self.home_url)


if __name__ == "__main__":
    unittest.main()
