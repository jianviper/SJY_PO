#!/usr/bin/env python
#coding:utf-8
import unittest
from common.get_config import get_url
from pages.Page_wk_note import Note
from parts.fc_tool_worker import WorkerTool
from parts.fc_tool_page import PageTool
from time import sleep, ctime

'''
Create on 2020-12-5
author:linjian
summary:便签的测试用例
'''


class NoteTest(unittest.TestCase):
    def setUp(self) -> None:
        urls = get_url()  #return [url,home_url]
        self.url, self.home_url = urls[0], urls[1]
        self.username = '14500000050'
        self.password = '123456'
        self.note_PO = Note(base_url=self.url)
        self.pg = PageTool(self.note_PO)
        self.projectName = self.pg.project_name()
        self.ele_tool = WorkerTool(self.note_PO)
        self.note_PO.open()

    def tearDown(self) -> None:
        self.pg.public_tearDown(self.url, self.home_url, self.username, self.password)
        self.note_PO.driver.quit()

    def add(self, num):
        #添加便签，点击
        self.pg.public_init(self.username, self.password, self.projectName)
        self.ele_tool.note_add(num=num)
        self.assertTrue(self.pg.public_check(self.note_PO.el_note_loc))
        self.pg.el_click(self.note_PO.el_note_loc)
        self.assertTrue(self.pg.public_check(self.note_PO.note_tool_loc))

    def test_add(self):
        '''添加便签'''
        self.add(1)
        bgColor = self.ele_tool.getCss(self.note_PO.el_note_box_loc, 'backgroundColor')
        self.assertEqual(bgColor, 'rgba(252, 252, 165, 1)')
        sleep(3)

    def test_edit(self):
        '''添加便签，点击T进入编辑'''
        self.add(1)
        #点击编辑按钮进入
        self.pg.el_click(self.note_PO.btn_edit_loc)
        self.assertTrue(self.pg.public_check(self.note_PO.rich_tool_loc))
        self.assertTrue(self.pg.public_check(self.note_PO.el_note_edit_loc))
        self.assertFalse(self.pg.public_check(self.note_PO.el_text_blur_loc))

    def test_changBgColor(self):
        '''添加便签，改变背景色'''
        self.add(1)
        self.note_PO.change_bgColor()

    def tes1t_changeSize(self):
        '''拖动改变尺寸'''
        self.add(1)
        btn_loc = self.ele_tool.getElPoi(self.note_PO.btn_Rsize_loc)[0]
        print(btn_loc)
        js_width = "return document.getElementsByClassName('note_box')[0].getClientRects()[0].width"
        js_height = "return document.getElementsByClassName('note_box')[0].getClientRects()[0].height"
        size1 = {'width': int(self.ele_tool.public_exJS(js_width)), 'height': int(self.ele_tool.public_exJS(js_height))}
        self.ele_tool.elDrag(self.note_PO.btn_Rsize_loc, btn_loc['x'] + 200, btn_loc['y'] + 200, self.note_PO)
        sleep(1)
        self.ele_tool.left_click(80, 100, self.note_PO.header_loc)
        size2 = {'width': int(self.ele_tool.public_exJS(js_width)), 'height': int(self.ele_tool.public_exJS(js_height))}
        print(size1, '\r\n', size2)

    def cut(self, num):
        self.add(num)
        if num > 1:
            self.ele_tool.selection(self.note_PO.el_note_loc)
        self.ele_tool.rightClick(el=self.note_PO.el_note_loc, action=self.note_PO.menu_cut_loc)
        self.assertFalse(self.pg.public_check(self.note_PO.el_note_loc))
        self.ele_tool.rightClick(500, 100, self.note_PO.header_loc, self.note_PO.menu_paste_loc)
        self.assertEqual(self.pg.public_check(self.note_PO.el_note_loc, islen=True), num)

    def test_cut(self):
        self.cut(2)

    def test_ty_cut(self):
        self.pg.tiyan()
        self.cut(2)

    def copy(self, num):
        self.add(num)
        if num > 1:
            self.ele_tool.selection(self.note_PO.el_note_loc)
        self.ele_tool.rightClick(el=self.note_PO.el_note_loc, action=self.note_PO.menu_copy_loc)
        self.ele_tool.rightClick(500, 100, self.note_PO.header_loc, self.note_PO.menu_paste_loc)
        self.assertEqual(self.pg.public_check(self.note_PO.el_note_loc, islen=True), num * 2)

    def test_copy(self):
        self.copy(2)

    def test_rich_style(self):
        '''富文本-加粗，斜体，下划线'''
        self.add(1)
        self.pg.el_click(self.note_PO.btn_edit_loc)
        self.note_PO.input(self.pg.textNote_Content())
        self.ele_tool.left_click(type='sync')
        #富文本-加粗
        self.note_PO.check_rich_style(self.note_PO.rich_bold_loc, 'font-weight', '700')
        #富文本-斜体
        self.note_PO.check_rich_style(self.note_PO.rich_italic_loc, 'fontStyle', 'italic')
        #富文本-下划线
        self.note_PO.check_rich_style(self.note_PO.rich_underline_loc, 'textDecorationLine', 'underline')

    def test_ty_rich_style(self):
        self.pg.tiyan()
        self.ele_tool.note_add(text=self.pg.textNote_Content())
        #富文本-加粗
        self.note_PO.check_rich_style(self.note_PO.rich_bold_loc, 'font-weight', '700')
        #富文本-斜体
        self.note_PO.check_rich_style(self.note_PO.rich_italic_loc, 'fontStyle', 'italic')
        #富文本-下划线
        self.note_PO.check_rich_style(self.note_PO.rich_underline_loc, 'textDecorationLine', 'underline')

    def test_rich_fontColor(self):
        '''富文本-字体颜色'''
        self.add(1)
        self.pg.el_click(self.note_PO.btn_edit_loc)
        self.note_PO.input(self.pg.textNote_Content())
        self.pg.el_click(self.note_PO.rich_fontColor_loc)
        #改变字体颜色
        self.note_PO.check_rich_fontColor()


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(NoteTest('test_ty_rich_style'))
    unittest.TextTestRunner().run(suite)
