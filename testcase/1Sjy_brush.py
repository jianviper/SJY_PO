#!/usr/bin/env python
#coding:utf-8
import unittest
from time import strftime, localtime
from pages.Page_worker import WorkerPage
from parts.tool_page import *

'''
Create on 2020-3-17
author:linjian
summary:画笔和橡皮擦的测试用例
'''


class WorkerTest(unittest.TestCase):
    linexy = []

    def setUp(self) -> None:
        url = 'https://app.bimuyu.tech/login'
        #url = 'http://test.bimuyu.tech/login'
        self.home_url = 'http://app.bimuyu.tech/home'
        self.username = '14500000050'
        self.password = '123456'
        self.brushPage = WorkerPage(base_url=url)
        self._nowtime = strftime("%Y-%m-%d %H:%M:%S", localtime())
        self.projectName = '自动化测试项目-{0}'.format(self._nowtime)
        self.textContent = '自动化测试文本-{0}'.format(self._nowtime)
        self.lineNum = 5

    def tearDown(self) -> None:
        self.brushPage.driver.get(self.home_url)
        if self.brushPage.check((By.CLASS_NAME, 'item_text'), islen=True) > 2:
            pass
            # public_delProject(self.brushPage, self.home_url)
        self.brushPage.driver.quit()

    def test_draw(self):
        '''使用画笔绘制'''
        public_login(self.brushPage, self.username, self.password)
        public_createProject(self.brushPage, self.projectName)
        self.brushPage.click_intoProject()
        self.brushPage.choose_tool(self.brushPage.tool_pen_loc)
        n = i = self.lineNum
        sleep(3)
        self.brushPage.action_click(self.brushPage.svg_loc)
        while i > 0:  #绘制多条痕迹
            # self.linexy.append(self.brushPage.draw_line())
            self.linexy.append(self.brushPage.draw_line())
            i -= 1
            sleep(1)
        print(self.projectName, '\r\n', self.linexy)
        self.assertEqual(n, self.brushPage.check(self.brushPage.el_line_loc, islen=True))  #检查是否绘制成功
        sleep(3)

    def te1st_eraser(self):
        '''使用橡皮擦'''
        public_login(self.brushPage, self.username, self.password)
        public_createProject(self.brushPage, self.projectName)
        self.brushPage.click_intoProject()
        self.brushPage.choose_tool(self.brushPage.tool_pen_loc)
        n = i = self.lineNum
        while i > 0:  #绘制多条痕迹
            self.linexy.append(self.brushPage.draw_line())
            i -= 1
            sleep(0.6)
        #检查是否绘制成功
        self.assertEqual(n, self.brushPage.check(self.brushPage.el_line_loc, islen=True))
        self.brushPage.choose_tool(self.brushPage.tool_pen_loc)
        self.brushPage.choose_tool(self.brushPage.tool_eraser_loc)
        print(self.linexy[0])
        self.brushPage.do_eraser(self.linexy[0])  #擦除第一根痕迹
        #是否擦除成功
        self.assertLess(self.brushPage.check(self.brushPage.el_line_loc, islen=True), self.lineNum)
        public_delProject(self.brushPage, self.home_url)
        sleep(3)

    def te1st_brush(self):

        public_login(self.brushPage, self.username, self.password)
        public_createProject(self.brushPage, self.projectName)
        self.brushPage.click_intoProject()
        self.brushPage.choose_tool(self.brushPage.tool_pen_loc)
        # print(self.brushPage.draw_line1())
        sleep(3)


if __name__ == "__main__":
    unittest.main()
'''
        token = self.WorkerPage.driver.get_cookies()[1]['value']
        url = 'https://api.hetaonote.com:8080/hetaoNoteApi/app/element/add'
        header = {'token': token,
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/79.0.3945.88 Safari/537.36'}
        data = {'parentId': 58535, 'position': '761,243', 'type': 2, 'html': 'test', 'content': '', 'ext': ''}
        requests.post(url, data,headers=header,verify = False)
'''
