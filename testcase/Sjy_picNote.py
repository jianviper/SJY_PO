#!/usr/bin/env python
#coding:utf-8
import unittest
from common.get_config import get_url
from pages.Page_wk_img import WokerPic
from parts.tool_worker import *
from parts.tool_page import tiyan

'''
Create on 2020-4-7
author:linjian
summary:图片便签的测试用例(不通过工具栏添加)
'''


class ImgNoteTest(unittest.TestCase):
    def setUp(self) -> None:
        urls = get_url()  #return [url,home_url]
        self.url, self.home_url = urls[0], urls[1]
        self.username = '14500000050'
        self.password = '123456'
        self.pic_PO = WokerPic(base_url=self.url)
        self.projectName = project_name()
        self.textContent = text_Content()
        self.pic_PO.open()

    def tearDown(self) -> None:
        public_tearDown(self.pic_PO, self.url, self.home_url, self.username, self.password)
        self.pic_PO.driver.quit()

    def test_add(self):
        '''添加图片便签'''
        public_init(self.pic_PO, self.username, self.password, self.projectName)
        ws_add(self.pic_PO, [('i', 1)])
        self.assertTrue(public_check(self.pic_PO, self.pic_PO.el_img_loc, attr='src'))
        el_click(self.pic_PO, self.pic_PO.el_imgDIV_loc)
        self.assertTrue(public_check(self.pic_PO, self.pic_PO.tool_imgTool_loc))

    def cut(self, num):
        ws_add(self.pic_PO, [('i', num)])
        self.assertTrue(public_check(self.pic_PO, self.pic_PO.el_img_loc, attr='src'))
        poi_src = public_getElPoi(self.pic_PO, self.pic_PO.el_imgDIV_loc)
        if num > 1:
            selection(self.pic_PO, self.pic_PO.el_imgDIV_loc)  #多选，下一步进行剪切
        rightClick(self.pic_PO, el=self.pic_PO.el_imgDIV_loc, action=self.pic_PO.btn_imgCut_loc)
        #检查是否剪切成功
        self.assertFalse(public_check(self.pic_PO, self.pic_PO.el_imgDIV_loc))
        left_click(self.pic_PO, 200, 50, el=self.pic_PO.tool_loc)
        #剪切成功后左键点击画布，检查是否有出现元素（BUG点）
        self.assertEqual(public_check(self.pic_PO, self.pic_PO.el_divs_loc, islen=True), 0)
        rightClick(self.pic_PO, action=self.pic_PO.btn_Paste_loc)
        self.assertEqual(public_check(self.pic_PO, self.pic_PO.el_imgDIV_loc, islen=True), num)
        poi_dst = public_getElPoi(self.pic_PO, self.pic_PO.el_imgDIV_loc)
        public_revoke_recovery(self.pic_PO, self.pic_PO.el_imgDIV_loc, type='cut', poi_src=poi_src, poi_dst=poi_dst)

    def test_cut(self):
        '''单张剪切/粘贴'''
        public_init(self.pic_PO, self.username, self.password, self.projectName)
        self.cut(1)

    def test_ty_cut(self):
        '''体验模式-单张剪切/粘贴'''
        tiyan(self.pic_PO)
        self.cut(1)

    def test_multicut(self):
        '''多选剪切，粘贴'''
        public_init(self.pic_PO, self.username, self.password, self.projectName)
        self.cut(2)

    def test_ty_multicut(self):
        '''体验模式-多选剪切，粘贴'''
        tiyan(self.pic_PO)
        self.cut(2)

    def copy(self, num):
        #图片便签的复制粘贴
        ws_add(self.pic_PO, [('i', num)])
        self.assertTrue(public_check(self.pic_PO, self.pic_PO.el_img_loc, attr='src'))
        poi_src = public_getElPoi(self.pic_PO, self.pic_PO.el_imgDIV_loc)
        if num > 1:
            selection(self.pic_PO, self.pic_PO.el_imgDIV_loc)  #多选，下一步进行复制
        rightClick(self.pic_PO, el=self.pic_PO.el_imgDIV_loc, action=self.pic_PO.btn_imgCopy_loc)
        left_click(self.pic_PO, 600, 100, el=self.pic_PO.header_loc)
        rightClick(self.pic_PO, action=self.pic_PO.btn_Paste_loc)
        self.assertEqual(public_check(self.pic_PO, self.pic_PO.el_imgDIV_loc, islen=True), num * 2)
        public_revoke_recovery(self.pic_PO, self.pic_PO.el_imgDIV_loc, type='copy', num=num)

    def test_copy(self):
        '''单张复制，粘贴'''
        public_init(self.pic_PO, self.username, self.password, self.projectName)
        self.copy(1)

    def test_multiCopy(self):
        '''多张复制，粘贴'''
        public_init(self.pic_PO, self.username, self.password, self.projectName)
        self.copy(2)

    def tes1t_drag(self):
        '''拖动到文件夹内'''
        public_init(self.pic_PO, self.username, self.password, self.projectName)
        ws_add(self.pic_PO, [('i', 1)])
        self.pic_PO.driver.refresh()
        self.assertTrue(public_check(self.pic_PO, self.pic_PO.el_img_loc, attr='src'))
        #添加文件夹
        public_addTool(self.pic_PO, self.pic_PO.tool_folder_loc, self.pic_PO.el_folder_loc, x=300, y=500)
        self.assertTrue(public_check(self.pic_PO, self.pic_PO.el_folder_loc))
        #拖动文本到文件夹内
        elDrag(self.pic_PO, self.pic_PO.el_img_loc, self.pic_PO.el_folder_loc)
        # self.assertFalse(public_check(self.pic_PO,self.pic_PO.el_text_loc))

        public_delProject(self.pic_PO, self.home_url)

    def rotate(self, type):
        #旋转图片,type:1 右键-旋转,type:2 工具栏-旋转
        ws_add(self.pic_PO, [('i', 1)])
        size1 = public_getElSize(self.pic_PO, self.pic_PO.el_imgDIV_loc)
        if type == 1:  #右键-旋转
            rightClick(self.pic_PO, el=self.pic_PO.el_imgDIV_loc, action=self.pic_PO.btn_imgRorate_loc)
        elif type == 2:  #工具栏-旋转
            el_click(self.pic_PO, self.pic_PO.el_imgDIV_loc)
            el_click(self.pic_PO, self.pic_PO.btn_tool_rorate_loc)
        size2 = public_getElSize(self.pic_PO, self.pic_PO.el_imgDIV_loc)
        #点击图片宽高会加2px
        self.assertTrue(size1[0]['height'] == size2[0]['width'])
        self.assertTrue(size2[0]['height'] == size1[0]['width'])
        public_revoke_recovery(self.pic_PO, self.pic_PO.el_imgDIV_loc, type='rotate', size1=size1, size2=size2)

    def test_right_rotate(self):
        '''右键-旋转图片'''
        public_init(self.pic_PO, self.username, self.password, self.projectName)
        self.rotate(1)

    def test_tool_rotate(self):
        '''工具栏-旋转图片'''
        public_init(self.pic_PO, self.username, self.password, self.projectName)
        self.rotate(2)

    def tes1t_ty_rotate(self):
        '''体验模式-右键-旋转图片'''
        tiyan(self.pic_PO)
        self.rotate(1)

    def origin(self, type):
        #原图尺寸,type:1 右键,type:2 工具栏
        ws_add(self.pic_PO, [('i', 1)])
        size1 = public_getElSize(self.pic_PO, self.pic_PO.el_imgDIV_loc)
        if type == 1:
            rightClick(self.pic_PO, el=self.pic_PO.el_imgDIV_loc, action=self.pic_PO.btn_imgOrigin_loc)
        elif type == 2:
            el_click(self.pic_PO, self.pic_PO.el_imgDIV_loc)
            el_click(self.pic_PO, self.pic_PO.btn_tool_orign_loc)
        size2 = public_getElSize(self.pic_PO, self.pic_PO.el_imgDIV_loc)
        self.assertTrue(size1[0]['width'] < size2[0]['width'])
        self.assertTrue(size1[0]['height'] < size2[0]['height'])
        public_revoke_recovery(self.pic_PO, self.pic_PO.el_imgDIV_loc, type='origin', size1=size1, size2=size2)

    def test_right_origin(self):
        '''右键-原图尺寸'''
        public_init(self.pic_PO, self.username, self.password, self.projectName)
        self.origin(1)

    def test_tool_origin(self):
        '''工具栏-原图尺寸'''
        public_init(self.pic_PO, self.username, self.password, self.projectName)
        self.origin(2)

    def tes1t_ty_origin(self):
        '''体验模式-原图尺寸'''
        tiyan(self.pic_PO)
        self.origin(1)


if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestSuite()
    # suite.addTest(ImgNoteTest('test_add'))
    # unittest.TextTestRunner().run(suite)
