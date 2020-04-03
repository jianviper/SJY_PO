#!/usr/bin/env python
#coding:utf-8
import unittest,os
from time import sleep,strftime,localtime
from pages.Page_worker import WorkerPage
from parts.login_ps import publicLogin
from parts.homePage_ps import public_createProject, public_delProject

'''
Create on 2020-3-17
author:linjian
summary:Home页的测试用例
'''


class WorkerTest(unittest.TestCase):
    linexy = []

    def setUp(self) -> None:
        url = 'https://app.bimuyu.tech/login'
        #url = 'http://test.bimuyu.tech/login'
        self.username = '14500000050'
        self.password = '123456'
        self.WorkerPage = WorkerPage(base_url=url)
        self._nowtime=strftime("%Y-%m-%d %H:%M:%S", localtime())
        self.projectName = '自动化测试项目-{0}'.format(self._nowtime)
        self.textContent = '自动化测试文本-{0}'.format(self._nowtime)
        self.WorkerPage.create_action()
        self.lineNum = 5

    def tearDown(self) -> None:
        public_delProject(self.WorkerPage)
        self.WorkerPage.driver.quit()

    def te1st_draw(self):
        '''使用画笔绘制'''
        publicLogin(self.WorkerPage, self.username, self.password)
        public_createProject(self.WorkerPage, self.projectName)
        self.WorkerPage.click_intoProject()
        self.WorkerPage.choose_tool(self.WorkerPage.tool_pen_loc)
        n = i = self.lineNum
        while i > 0:  #绘制多条痕迹
            self.linexy.append(self.WorkerPage.draw_line())
            i -= 1
            sleep(0.6)
        self.assertEqual(n, self.WorkerPage.check(self.WorkerPage.el_line_loc,islen=True))  #检查是否绘制成功
        print(self.projectName, '\r\n', self.linexy)
        sleep(3)

    def te1st_eraser(self):
        '''使用橡皮擦'''
        print(self.linexy)
        publicLogin(self.WorkerPage, self.username, self.password)
        public_createProject(self.WorkerPage, self.projectName)
        self.WorkerPage.click_intoProject()
        self.WorkerPage.choose_tool(self.WorkerPage.tool_pen_loc)
        n = i = self.lineNum
        while i > 0:  #绘制多条痕迹
            self.linexy.append(self.WorkerPage.draw_line())
            i -= 1
            sleep(0.6)
        self.WorkerPage.choose_tool(self.WorkerPage.tool_pen_loc)
        self.WorkerPage.choose_tool(self.WorkerPage.tool_eraser_loc)
        self.WorkerPage.do_eraser(self.linexy[0]) #擦除第一根痕迹
        #是否擦除成功
        self.assertLess(self.WorkerPage.check(self.WorkerPage.el_line_loc,islen=True), self.lineNum)
        self.WorkerPage.driver.back()
        self.WorkerPage.driver.refresh()
        public_delProject(self.WorkerPage)
        sleep(3)

    def te1st_add_text(self):
        '''添加文本便签,若成功，添加内容'''
        publicLogin(self.WorkerPage, self.username, self.password)
        public_createProject(self.WorkerPage, self.projectName)
        self.WorkerPage.click_intoProject()
        self.WorkerPage.choose_tool(self.WorkerPage.tool_text_loc)
        self.WorkerPage.action_click(200, -200)
        #是否新建成功
        self.assertTrue(self.WorkerPage.check(self.WorkerPage.el_textNote_loc))
        self.WorkerPage.input_textNote(self.textContent) #点击文本便签，再输入文本
        self.WorkerPage.pyag_click() #点击画布
        self.assertTrue(self.WorkerPage.check(self.WorkerPage.el_textNoteContent_loc, self.textContent))
        self.WorkerPage.driver.refresh()
        #刷新页面数据是否还在
        self.assertTrue(self.WorkerPage.check(self.WorkerPage.el_textNoteContent_loc, self.textContent))
        self.WorkerPage.driver.back()
        self.WorkerPage.driver.refresh()
        public_delProject(self.WorkerPage)
        sleep(3)

    def te1st_del_text(self):
        '''删除文本便签'''
        publicLogin(self.WorkerPage, self.username, self.password)
        public_createProject(self.WorkerPage, self.projectName)
        self.WorkerPage.click_intoProject()
        self.WorkerPage.choose_tool(self.WorkerPage.tool_text_loc)
        self.WorkerPage.action_click(200, -200)
        #是否新建成功
        self.assertTrue(self.WorkerPage.check(self.WorkerPage.el_textNote_loc))
        self.WorkerPage.del_el(self.WorkerPage.el_textNote_loc)
        #是否删除成功
        self.assertFalse(self.WorkerPage.check(self.WorkerPage.el_textNote_loc))
        self.WorkerPage.driver.back()
        self.WorkerPage.driver.refresh()
        public_delProject(self.WorkerPage)
        sleep(3)

    def test_add_imgNote(self):
        '''添加图片便签'''
        publicLogin(self.WorkerPage, self.username, self.password)
        public_createProject(self.WorkerPage, self.projectName)
        self.WorkerPage.click_intoProject()
        self.WorkerPage.choose_tool(self.WorkerPage.tool_img_loc)
        self.WorkerPage.action_click(200,-200)
        #是否新建成功
        self.assertTrue(self.WorkerPage.check(self.WorkerPage.el_img_loc))
        self.WorkerPage.click_imgUpload()
        os.system('uploadIMG.exe')
        sleep(5)
        #是否上传成功
        self.assertTrue(self.WorkerPage.check(self.WorkerPage.el_uploadImg_loc))
        self.WorkerPage.del_el(self.WorkerPage.el_img_loc)
        #是否删除成功
        self.assertFalse(self.WorkerPage.check(self.WorkerPage.el_img_loc))
        self.WorkerPage.driver.back()
        self.WorkerPage.driver.refresh()
        public_delProject(self.WorkerPage)
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
