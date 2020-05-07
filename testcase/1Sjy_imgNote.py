#!/usr/bin/env python
#coding:utf-8
import unittest
from time import strftime, localtime
from pages.Page_wk_img import WokerPic
from parts.tool_worker import *

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
        self.img_PO = WokerPic(base_url=url)
        self._nowtime = strftime("%Y-%m-%d %H:%M:%S", localtime())
        self.projectName = '自动化测试项目-{0}'.format(self._nowtime)
        self.textContent = '自动化测试文本-{0}'.format(self._nowtime)
        self.img_PO.open()

    def tearDown(self) -> None:
        self.img_PO.driver.get(self.home_url)
        if public_check(self.img_PO, (By.CLASS_NAME, 'item_text'), islen=True) > 2:
            public_delProject(self.img_PO, self.home_url)
        self.img_PO.driver.quit()

    def test_add_imgNote(self):
        '''添加/上传/删除/恢复图片便签'''
        public_login(self.img_PO, self.username, self.password)
        public_createProject(self.img_PO, self.projectName)
        public_intoProject(self.img_PO)
        public_addTool(self.img_PO, self.img_PO.tool_img_loc, self.img_PO.el_imgDIV_loc, action='upload')
        #是否上传成功
        self.assertTrue(public_check(self.img_PO, self.img_PO.el_img_loc))
        rightClick_action(self.img_PO, el=self.img_PO.el_imgDIV_loc, actionEl=self.img_PO.btn_del_loc)
        #是否删除成功
        self.assertFalse(public_check(self.img_PO, self.img_PO.el_imgDIV_loc))
        click_trash(self.img_PO)  #打开废纸篓进行恢复
        recovery(self.img_PO)
        #检查恢复是否成功
        self.assertTrue(public_check(self.img_PO, self.img_PO.el_imgDIV_loc))
        sleep(3)
        public_delProject(self.img_PO, self.home_url)

    def test_replace(self):
        '''替换图片'''
        public_login(self.img_PO, self.username, self.password)
        public_createProject(self.img_PO, self.projectName)
        public_intoProject(self.img_PO)
        public_addTool(self.img_PO, self.img_PO.tool_img_loc, self.img_PO.el_imgDIV_loc, action='upload')
        #是否上传成功
        self.assertTrue(public_check(self.img_PO, self.img_PO.el_img_loc))
        src1 = self.img_PO.get_imgSrc()
        #右键-替换
        rightClick_action(self.img_PO, el=self.img_PO.el_imgDIV_loc, actionEl=self.img_PO.btn_tihuan_loc)
        os.system('uploadIMG.exe')
        sleep(5)
        src2 = self.img_PO.get_imgSrc()
        self.assertNotEqual(src1, src2)  #判断图片替换是否成功
        sleep(3)
        public_delProject(self.img_PO, self.home_url)

    def test_shear(self):
        '''剪切,粘贴'''
        public_login(self.img_PO, self.username, self.password)
        public_createProject(self.img_PO, self.projectName)
        public_intoProject(self.img_PO)
        public_addTool(self.img_PO, self.img_PO.tool_img_loc, self.img_PO.el_imgDIV_loc)
        rightClick_action(self.img_PO, el=self.img_PO.el_imgDIV_loc, actionEl=self.img_PO.btn_jianqie_loc)
        #检查剪切是否成功
        self.assertFalse(public_check(self.img_PO, self.img_PO.el_imgDIV_loc))
        #剪切后左键点击画布，检查是否会有文件夹多出（BUG点）
        left_click(self.img_PO, 200, 50, el=self.img_PO.tool_loc)
        self.assertTrue(public_check(self.img_PO, self.img_PO.el_divs_loc, islen=True) == 2)
        rightClick_action(self.img_PO, actionEl=self.img_PO.btn_zhantie_loc)
        self.assertTrue(public_check(self.img_PO, self.img_PO.el_imgDIV_loc))
        sleep(3)
        public_delProject(self.img_PO, self.home_url)

    def test_multiShear(self):
        '''多选剪切，粘贴'''
        public_login(self.img_PO, self.username, self.password)
        public_createProject(self.img_PO, self.projectName)
        public_intoProject(self.img_PO)
        public_addTool(self.img_PO, self.img_PO.tool_img_loc, self.img_PO.el_imgDIV_loc, nums=2, action='upload')
        #是否上传成功
        self.assertTrue(public_check(self.img_PO, self.img_PO.el_img_loc, islen=True) == 2)
        selection(self.img_PO, self.img_PO.el_imgDIV_loc)  #多选，下一步进行剪切
        rightClick_action(self.img_PO, el=self.img_PO.el_imgDIV_loc, actionEl=self.img_PO.btn_jianqie_loc)
        #检查是否剪切成功
        self.assertFalse(public_check(self.img_PO, self.img_PO.el_imgDIV_loc))
        left_click(self.img_PO, 200, 50, el=self.img_PO.tool_loc)
        #剪切成功后左键点击画布，检查是否有出现元素（BUG点）
        self.assertTrue(public_check(self.img_PO, self.img_PO.el_divs_loc, islen=True) == 2)
        rightClick_action(self.img_PO, actionEl=self.img_PO.btn_zhantie_loc)
        self.assertTrue(public_check(self.img_PO, self.img_PO.el_imgDIV_loc, islen=True) == 2)
        sleep(3)
        public_delProject(self.img_PO, self.home_url)

    def test_multiDel(self):
        '''多选删除,恢复'''
        public_login(self.img_PO, self.username, self.password)
        public_createProject(self.img_PO, self.projectName)
        public_intoProject(self.img_PO)
        public_addTool(self.img_PO, self.img_PO.tool_img_loc, self.img_PO.el_imgDIV_loc, nums=2, action='upload')
        #检查是否上传成功
        self.assertTrue(public_check(self.img_PO, self.img_PO.el_img_loc, islen=True) == 2)
        selection(self.img_PO, self.img_PO.el_imgDIV_loc)
        rightClick_action(self.img_PO, el=self.img_PO.el_imgDIV_loc, actionEl=self.img_PO.btn_del_loc)
        #是否删除成功
        self.assertFalse(public_check(self.img_PO, self.img_PO.el_imgDIV_loc))
        click_trash(self.img_PO)  #打开废纸篓进行恢复
        recovery(self.img_PO)
        #检查恢复是否成功
        self.assertTrue(public_check(self.img_PO, self.img_PO.el_imgDIV_loc, islen=True) == 2)
        sleep(3)
        public_delProject(self.img_PO, self.home_url)


if __name__ == "__main__":
    unittest.main()
