#!/usr/bin/env python
#coding:utf-8
import unittest
from time import strftime, localtime
from pages.Page_worker import WorkerPage
from parts.pageTools import *

'''
Create on 2020-4-7
author:linjian
summary:图片便签的测试用例
'''


class ImgNoteTest(unittest.TestCase):
    def setUp(self) -> None:
        url = 'https://app.bimuyu.tech/login'
        #url = 'http://test.bimuyu.tech/login'
        self.home_url = 'https://app.bimuyu.tech/home'
        self.username = '14500000050'
        self.password = '123456'
        self.imgPO = WorkerPage(base_url=url)
        self._nowtime = strftime("%Y-%m-%d %H:%M:%S", localtime())
        self.projectName = '自动化测试项目-{0}'.format(self._nowtime)
        self.textContent = '自动化测试文本-{0}'.format(self._nowtime)
        self.imgPO.open()

    def tearDown(self) -> None:
        self.imgPO.driver.get(self.home_url)
        if self.imgPO.check((By.CLASS_NAME, 'item_text'), islen=True) > 2:
            public_delProject(self.imgPO, self.home_url)
        self.imgPO.driver.quit()

    def test_add_imgNote(self):
        '''添加/上传/删除/恢复图片便签'''
        public_login(self.imgPO, self.username, self.password)
        public_createProject(self.imgPO, self.projectName)
        self.imgPO.click_intoProject()
        public_addTool(self.imgPO, self.imgPO.tool_img_loc,self.imgPO.el_imgDIV_loc,action='upload')
        #是否上传成功
        self.assertTrue(self.imgPO.check(self.imgPO.el_img_loc))
        self.imgPO.rightClick_action(el=self.imgPO.el_imgDIV_loc, actionEL=self.imgPO.btn_del_loc)
        #是否删除成功
        self.assertFalse(self.imgPO.check(self.imgPO.el_imgDIV_loc))
        self.imgPO.click_trash()
        self.imgPO.recovery()
        #检查恢复是否成功
        self.assertTrue(self.imgPO.check(self.imgPO.el_imgDIV_loc))
        sleep(3)
        public_delProject(self.imgPO, self.home_url)

    def test_replace(self):
        '''替换图片'''
        public_login(self.imgPO, self.username, self.password)
        public_createProject(self.imgPO, self.projectName)
        self.imgPO.click_intoProject()
        public_addTool(self.imgPO, self.imgPO.tool_img_loc,self.imgPO.el_imgDIV_loc,action='upload')
        #是否上传成功
        self.assertTrue(self.imgPO.check(self.imgPO.el_img_loc))
        src1 = self.imgPO.get_imgSrc()
        #右键-替换
        self.imgPO.rightClick_action(el=self.imgPO.el_imgDIV_loc, actionEL=self.imgPO.btn_tihuan_loc)
        os.system('uploadIMG.exe')
        sleep(5)
        src2 = self.imgPO.get_imgSrc()
        self.assertNotEqual(src1, src2)  #判断图片替换是否成功
        sleep(3)
        public_delProject(self.imgPO, self.home_url)

    def test_shear(self):
        '''剪切,粘贴'''
        public_login(self.imgPO, self.username, self.password)
        public_createProject(self.imgPO, self.projectName)
        self.imgPO.click_intoProject()
        public_addTool(self.imgPO, self.imgPO.tool_img_loc,self.imgPO.el_imgDIV_loc)
        self.imgPO.rightClick_action(el=self.imgPO.el_imgDIV_loc, actionEL=self.imgPO.btn_jianqie_loc)
        #检查剪切是否成功
        self.assertFalse(self.imgPO.check(self.imgPO.el_imgDIV_loc))
        #剪切后左键点击画布，检查是否会有文件夹多出（BUG点）
        self.imgPO.action_click(200, 50, el=self.imgPO.tool_loc)
        self.assertTrue(self.imgPO.check(self.imgPO.el_divs_loc, islen=True) == 2)
        self.imgPO.rightClick_action(actionEL=self.imgPO.btn_zhantie_loc)
        self.assertTrue(self.imgPO.check(self.imgPO.el_imgDIV_loc))
        sleep(3)
        public_delProject(self.imgPO, self.home_url)

    def test_multiShear(self):
        '''多选剪切，粘贴'''
        public_login(self.imgPO, self.username, self.password)
        public_createProject(self.imgPO, self.projectName)
        self.imgPO.click_intoProject()
        public_addTool(self.imgPO, self.imgPO.tool_img_loc,self.imgPO.el_imgDIV_loc, nums=2,action='upload')
        #是否上传成功
        self.assertTrue(self.imgPO.check(self.imgPO.el_img_loc, islen=True) == 2)
        self.imgPO.selection(self.imgPO.el_imgDIV_loc) #多选，下一步进行剪切
        self.imgPO.rightClick_action(el=self.imgPO.el_imgDIV_loc, actionEL=self.imgPO.btn_jianqie_loc)
        #检查是否剪切成功
        self.assertFalse(self.imgPO.check(self.imgPO.el_imgDIV_loc))
        self.imgPO.action_click(200, 50, el=self.imgPO.tool_loc)
        #剪切成功后左键点击画布，检查是否有出现元素（BUG点）
        self.assertTrue(self.imgPO.check(self.imgPO.el_divs_loc, islen=True) == 2)
        self.imgPO.rightClick_action(actionEL=self.imgPO.btn_zhantie_loc)
        self.assertTrue(self.imgPO.check(self.imgPO.el_imgDIV_loc, islen=True) == 2)
        sleep(3)
        public_delProject(self.imgPO, self.home_url)

    def test_multiDel(self):
        '''多选删除,恢复'''
        public_login(self.imgPO, self.username, self.password)
        public_createProject(self.imgPO, self.projectName)
        self.imgPO.click_intoProject()
        public_addTool(self.imgPO, self.imgPO.tool_img_loc,self.imgPO.el_imgDIV_loc, nums=2, action='upload')
        #检查是否上传成功
        self.assertTrue(self.imgPO.check(self.imgPO.el_img_loc, islen=True) == 2)
        self.imgPO.selection(self.imgPO.el_imgDIV_loc)
        self.imgPO.rightClick_action(el=self.imgPO.el_imgDIV_loc, actionEL=self.imgPO.btn_del_loc)
        #是否删除成功
        self.assertFalse(self.imgPO.check(self.imgPO.el_imgDIV_loc))
        self.imgPO.click_trash()
        self.imgPO.recovery()
        #检查恢复是否成功
        self.assertTrue(self.imgPO.check(self.imgPO.el_imgDIV_loc, islen=True) == 2)
        sleep(3)
        public_delProject(self.imgPO, self.home_url)


if __name__ == "__main__":
    unittest.main()
