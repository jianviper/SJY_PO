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
        self.textContent = textNote_Content()
        self.pic_PO.open()

    def tearDown(self) -> None:
        public_tearDown(self.pic_PO, self.url, self.home_url, self.username, self.password)
        self.pic_PO.driver.quit()

    def Del(self, num):
        #删除图片便签
        public_add(self.pic_PO, [('i', num)])
        self.assertTrue(public_check(self.pic_PO, self.pic_PO.el_img_loc, attr='src'))
        public_revoke(self.pic_PO, self.pic_PO.el_imgDIV_loc, step=num)
        if num > 1:
            selection(self.pic_PO, self.pic_PO.el_imgDIV_loc)
        rightClick(self.pic_PO, el=self.pic_PO.el_imgDIV_loc, action=self.pic_PO.btn_imgDel_loc)
        #是否删除成功
        self.assertFalse(public_check(self.pic_PO, self.pic_PO.el_imgDIV_loc))
        public_revoke(self.pic_PO, self.pic_PO.el_imgDIV_loc, type='del')
        # click_trash(self.pic_PO)  #打开废纸篓进行恢复
        # recovery(self.pic_PO)
        #检查恢复是否成功
        # self.assertTrue(public_check(self.pic_PO, self.pic_PO.el_imgDIV_loc, islen=True) == 1)

    def test_del(self):
        '''单张删除/恢复'''
        public_init(self.pic_PO, self.username, self.password, self.projectName)
        self.Del(1)
        public_delProject(self.pic_PO, self.home_url)

    def test_ty_del(self):
        '''体验模式-单张删除/恢复'''
        tiyan(self.pic_PO)
        self.Del(1)

    def test_multiDel(self):
        '''多选删除/恢复'''
        public_init(self.pic_PO, self.username, self.password, self.projectName)
        self.Del(2)
        public_delProject(self.pic_PO, self.home_url)

    def test_ty_multiDel(self):
        '''体验模式-多选删除/恢复'''
        tiyan(self.pic_PO)
        self.Del(2)

    def cut(self, num):
        public_add(self.pic_PO, [('i', num)])
        self.assertTrue(public_check(self.pic_PO, self.pic_PO.el_img_loc, attr='src'))
        poi_src = public_getElPosition(self.pic_PO, self.pic_PO.el_imgDIV_loc)
        if num > 1:
            selection(self.pic_PO, self.pic_PO.el_imgDIV_loc)  #多选，下一步进行剪切
        rightClick(self.pic_PO, el=self.pic_PO.el_imgDIV_loc, action=self.pic_PO.btn_imgCut_loc)
        #检查是否剪切成功
        self.assertFalse(public_check(self.pic_PO, self.pic_PO.el_imgDIV_loc))
        left_click(self.pic_PO, 200, 50, el=self.pic_PO.tool_loc)
        #剪切成功后左键点击画布，检查是否有出现元素（BUG点）
        self.assertIs(public_check(self.pic_PO, self.pic_PO.el_divs_loc, islen=True), 0)
        rightClick(self.pic_PO, action=self.pic_PO.btn_Paste_loc)
        self.assertIs(public_check(self.pic_PO, self.pic_PO.el_imgDIV_loc, islen=True), num)
        poi_dst = public_getElPosition(self.pic_PO, self.pic_PO.el_imgDIV_loc)
        public_revoke(self.pic_PO, self.pic_PO.el_imgDIV_loc, type='cut', poi_src=poi_src, poi_dst=poi_dst)

    def test_cut(self):
        '''单张剪切/粘贴'''
        public_init(self.pic_PO, self.username, self.password, self.projectName)
        self.cut(1)
        public_delProject(self.pic_PO, self.home_url)

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

    def tes1t_drag(self):
        '''拖动到文件夹内'''
        public_init(self.pic_PO, self.username, self.password, self.projectName)
        public_add(self.pic_PO, [('i', 1)])
        self.pic_PO.driver.refresh()
        self.assertTrue(public_check(self.pic_PO, self.pic_PO.el_img_loc, attr='src'))
        #添加文件夹
        public_addTool(self.pic_PO, self.pic_PO.tool_folder_loc, self.pic_PO.el_folder_loc, x=300, y=500)
        self.assertTrue(public_check(self.pic_PO, self.pic_PO.el_folder_loc))
        #拖动文本便签到文件夹内
        elDrag(self.pic_PO, self.pic_PO.el_img_loc, self.pic_PO.el_folder_loc)
        # self.assertFalse(public_check(self.pic_PO,self.pic_PO.el_textNote_loc))

        public_delProject(self.pic_PO, self.home_url)

    def rotate(self):
        '''旋转图片'''
        public_add(self.pic_PO, [('i', 1)])
        size1 = public_getElSize(self.pic_PO, self.pic_PO.el_imgDIV_loc)
        rightClick(self.pic_PO, el=self.pic_PO.el_imgDIV_loc, action=self.pic_PO.btn_imgRorate_loc)
        size2 = public_getElSize(self.pic_PO, self.pic_PO.el_imgDIV_loc)
        self.assertTrue(size1[0]['height'] == size2[0]['width'])
        self.assertTrue(size2[0]['height'] == size1[0]['width'])
        public_revoke(self.pic_PO, self.pic_PO.el_imgDIV_loc, type='rotate', size1=size1, size2=size2)

    def test_rotate(self):
        public_init(self.pic_PO, self.username, self.password, self.projectName)
        self.rotate()

    def test_ty_rotate(self):
        tiyan(self.pic_PO)
        self.rotate()

    def multi_rotate(self):
        '''多选，旋转'''
        public_add(self.pic_PO, [('i', 2)])
        size1 = public_getElSize(self.pic_PO, self.pic_PO.el_imgDIV_loc)
        selection(self.pic_PO, self.pic_PO.el_imgDIV_loc)
        rightClick(self.pic_PO, el=self.pic_PO.el_imgDIV_loc, action=self.pic_PO.btn_imgMRorate_loc)
        size2 = public_getElSize(self.pic_PO, self.pic_PO.el_imgDIV_loc)
        for i in range(size1.__len__()):
            self.assertTrue(size1[i]['width'] == size2[i]['height'])
            self.assertTrue(size1[i]['height'] == size2[i]['width'])
        # public_revoke(self.pic_PO,self.pic_PO.el_imgDIV_loc)

    def test_multi_rotate(self):
        public_init(self.pic_PO, self.username, self.password, self.projectName)
        self.multi_rotate()

    def test_ty_multi_rotate(self):
        tiyan(self.pic_PO)
        self.multi_rotate()

    def origin(self):
        '''原图尺寸'''
        public_add(self.pic_PO, [('i', 1)])
        size1 = public_getElSize(self.pic_PO, self.pic_PO.el_imgDIV_loc)
        rightClick(self.pic_PO, el=self.pic_PO.el_imgDIV_loc, action=self.pic_PO.btn_imgOrigin_loc)
        size2 = public_getElSize(self.pic_PO, self.pic_PO.el_imgDIV_loc)
        self.assertTrue(size1[0]['width'] < size2[0]['width'])
        self.assertTrue(size1[0]['height'] < size2[0]['height'])
        public_revoke(self.pic_PO, self.pic_PO.el_imgDIV_loc, type='origin', size1=size1, size2=size2)

    def test_origin(self):
        public_init(self.pic_PO, self.username, self.password, self.projectName)
        self.origin()

    def test_ty_origin(self):
        tiyan(self.pic_PO)
        self.origin()

    def multi_origin(self):
        '''原图尺寸'''
        public_add(self.pic_PO, [('i', 2)])
        size1 = public_getElSize(self.pic_PO, self.pic_PO.el_imgDIV_loc)
        selection(self.pic_PO, self.pic_PO.el_imgDIV_loc)
        rightClick(self.pic_PO, el=self.pic_PO.el_imgDIV_loc, action=self.pic_PO.btn_imgMOrigin_loc)
        size2 = public_getElSize(self.pic_PO, self.pic_PO.el_imgDIV_loc)
        for i in range(size1.__len__()):
            self.assertTrue(size1[i]['width'] < size2[i]['width'])
            self.assertTrue(size1[i]['height'] < size2[i]['height'])

    def test_multi_origin(self):
        public_init(self.pic_PO, self.username, self.password, self.projectName)
        self.multi_origin()

    def test_ty_multi_origin(self):
        tiyan(self.pic_PO)
        self.multi_origin()


if __name__ == '__main__':
    unittest.main()
    # suite=unittest.TestSuite()
    # suite.addTest(ImgNoteTest('multi_origin'))
