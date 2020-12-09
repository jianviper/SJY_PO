#!/usr/bin/env python
#coding:utf-8
import unittest
from common.get_config import get_url
from pages.Page_worker import WorkerPage
from parts.tool_worker import *

'''
Create on 2020-5-29
author:linjian
summary:关联线的测试用例
'''


class LinkTest(unittest.TestCase):

    def setUp(self) -> None:
        urls = get_url()  #return [url,home_url]
        self.url, self.home_url = urls[0], urls[1]
        self.username = '14500000050'
        self.username2 = '14500000051'
        self.password = '123456'
        self.link_PO = WorkerPage(base_url=self.url)
        self.projectName = project_name()
        self.textContent = text_Content()
        self.link_PO.open()

    def tearDown(self) -> None:
        public_tearDown(self.link_PO, self.url, self.home_url, self.username, self.password)
        self.link_PO.driver.quit()

    def link(self, s, e, start, end):
        '''
        两个元素之间添加关联线
        :param el: 要添加的元素
        :param start: 起始元素
        :param end: 终止元素
        :return:
        '''
        public_init(self.link_PO, self.username, self.password, self.projectName)
        ws_add(self.link_PO, [(s, 1), (e, 1)])
        # self.link_PO.driver.refresh()
        self.assertTrue(public_check(self.link_PO, self.link_PO.el_divs_loc))
        el_click(self.link_PO, start)
        elDrag(self.link_PO, start=self.link_PO.btn_relB_loc, end=end)
        self.link_PO.driver.refresh()
        check1 = public_check(self.link_PO, self.link_PO.el_relline_loc)
        check2 = public_check(self.link_PO, self.link_PO.el_line_loc, driver=True)
        self.assertTrue(check1 or check2)

    def test_textToNote(self):
        self.link('t', 'n', self.link_PO.el_text_loc, self.link_PO.el_note_loc)

    def test_fileToNote(self):
        self.link('file', 'n', self.link_PO.el_file_loc, self.link_PO.el_note_loc)

    def test_imgToText(self):
        self.link('i', 't', self.link_PO.el_imgNote_loc, self.link_PO.el_text_loc)

    def test_noteToFolder(self):
        self.link('n', 'f', self.link_PO.el_note_loc, self.link_PO.el_folder_loc)

    def addLine(self, type, start):
        #从起点元素拉出关联线，再新建元素
        public_init(self.link_PO, self.username, self.password, self.projectName)
        ws_add(self.link_PO, [(type, 1)])
        el_click(self.link_PO, start)
        menu1, menu2 = None, None
        if start == self.link_PO.el_text_loc:  #如果起点是文本
            menu1 = self.link_PO.menu_forlder_loc
            menu2 = self.link_PO.menu_text_loc
        elif start == self.link_PO.el_folder_loc:  #如果起点是文件夹
            menu1 = self.link_PO.menu_text_loc
            menu2 = self.link_PO.menu_forlder_loc
        else:  #如果起点是图片便签或文件
            menu1 = self.link_PO.menu_text_loc
            menu2 = self.link_PO.menu_forlder_loc
        #拉出关联线
        elDrag(self.link_PO, self.link_PO.btn_relB_loc, 0, 100)
        el_click(self.link_PO, menu1)  #点击菜单选择添加的元素
        left_click(self.link_PO, 100, 100, self.link_PO.header_loc)
        self.assertTrue(public_check(self.link_PO, self.link_PO.el_line_loc, driver=True))
        el_click(self.link_PO, start)
        #拉出关联线
        elDrag(self.link_PO, self.link_PO.btn_relR_loc, 100, 0)
        el_click(self.link_PO, menu2)  #点击菜单选择添加的元素
        left_click(self.link_PO, 100, 100, self.link_PO.header_loc)
        self.link_PO.driver.refresh()
        self.assertEqual(public_check(self.link_PO, self.link_PO.el_line_loc, islen=True, driver=True), 2)

    def cutAndPaste(self):
        #框选剪切粘贴
        selection(self.link_PO, self.link_PO.el_divs_loc)
        rightClick(self.link_PO, el=self.link_PO.el_text_loc, action=self.link_PO.menu_cut_loc)
        self.assertFalse(public_check(self.link_PO, self.link_PO.el_divs_loc))
        self.assertFalse(public_check(self.link_PO, self.link_PO.el_line_loc, attr='data-id', driver=True))
        #粘贴，判断元素和关联线数量
        rightClick(self.link_PO, 200, 300, self.link_PO.header_loc, self.link_PO.menu_paste_loc)
        self.assertEqual(public_check(self.link_PO, self.link_PO.el_divs_loc, islen=True), 3)
        self.assertEqual(public_check(self.link_PO, self.link_PO.el_line_loc, islen=True, driver=True), 2)

    def copyAndPaste(self):
        #框选复制粘贴
        self.link_PO.driver.refresh()
        public_check(self.link_PO, self.link_PO.el_divs_loc)
        selection(self.link_PO, self.link_PO.el_divs_loc)
        rightClick(self.link_PO, el=self.link_PO.el_text_loc, action=self.link_PO.menu_copy_loc)
        #粘贴，判断元素和关联线数量
        rightClick(self.link_PO, 400, 100, self.link_PO.header_loc, self.link_PO.menu_paste_loc)
        self.assertEqual(public_check(self.link_PO, self.link_PO.el_divs_loc, islen=True), 6)
        self.assertEqual(public_check(self.link_PO, self.link_PO.el_line_loc, islen=True, driver=True), 4)

    def tes1t_textNote(self):
        '''新建文本，拉出关联线'''
        self.addLine('t', self.link_PO.el_text_loc)
        poi_src = public_getElPoi(self.link_PO, self.link_PO.el_line_loc, driver=True)
        self.cutAndPaste()  #剪切，粘贴
        poi_dst = public_getElPoi(self.link_PO, self.link_PO.el_line_loc, driver=True)
        public_revoke_recovery(self.link_PO, self.link_PO.el_line_loc, type='cut', poi_src=poi_src, poi_dst=poi_dst,
                               driver=True)
        self.copyAndPaste()  #复制，粘贴
        public_revoke_recovery(self.link_PO, self.link_PO.el_line_loc, type='copy', driver=True, num=2)

    def tes1t_folder(self):
        '''新建文件夹，拉出关联线'''
        self.addLine('f', self.link_PO.el_folder_loc)
        poi_src = public_getElPoi(self.link_PO, self.link_PO.el_line_loc, driver=True)
        self.cutAndPaste()  #剪切，粘贴
        poi_dst = public_getElPoi(self.link_PO, self.link_PO.el_line_loc, driver=True)
        public_revoke_recovery(self.link_PO, self.link_PO.el_line_loc, type='cut', poi_src=poi_src, poi_dst=poi_dst,
                               driver=True)
        self.copyAndPaste()  #复制，粘贴
        public_revoke_recovery(self.link_PO, self.link_PO.el_line_loc, type='copy', driver=True, num=2)

    def tes1t_file(self):
        '''添加文件，拉出关联线'''
        self.addLine('file', self.link_PO.el_file_loc)
        poi_src = public_getElPoi(self.link_PO, self.link_PO.el_line_loc, driver=True)
        self.cutAndPaste()  #剪切，粘贴
        poi_dst = public_getElPoi(self.link_PO, self.link_PO.el_line_loc, driver=True)
        public_revoke_recovery(self.link_PO, self.link_PO.el_line_loc, type='cut', poi_src=poi_src, poi_dst=poi_dst,
                               driver=True)
        self.copyAndPaste()  #复制，粘贴
        public_revoke_recovery(self.link_PO, self.link_PO.el_line_loc, type='copy', driver=True, num=2)

    def tes1t_imgNote(self):
        '''新建图片便签，拉出关联线'''
        self.addLine('i', self.link_PO.el_img_loc)
        poi_src = public_getElPoi(self.link_PO, self.link_PO.el_line_loc, driver=True)
        self.cutAndPaste()  #剪切，粘贴
        poi_dst = public_getElPoi(self.link_PO, self.link_PO.el_line_loc, driver=True)
        public_revoke_recovery(self.link_PO, self.link_PO.el_line_loc, type='cut', poi_src=poi_src, poi_dst=poi_dst,
                               driver=True)
        self.copyAndPaste()  #复制，粘贴
        public_revoke_recovery(self.link_PO, self.link_PO.el_line_loc, type='copy', driver=True, num=2)


if __name__ == "__main__":
    unittest.main()
    # suite = unittest.TestSuite()
    # suite.addTest(LinkTest('test_textToNote'))
    # unittest.TextTestRunner().run(suite)
