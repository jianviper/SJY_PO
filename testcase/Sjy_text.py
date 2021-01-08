#!/usr/bin/env python
#coding:utf-8
import unittest
from common.get_config import get_url
from pages.Page_wk_text import Text
from parts.threads import thread_open
from parts.tool_worker import *
from parts.tool_page import tiyan

from factory.elementFactory import ElementCreater

'''
Create on 2020-4-7
author:linjian
summary:文本的测试用例
'''


class TextTest(unittest.TestCase):
    def setUp(self) -> None:
        urls = get_url()  #return [url,home_url]
        self.url, self.home_url = urls[0], urls[1]
        self.username = '14500000050'
        self.username2 = '14500000051'
        self.password = '123456'
        self.text_PO = Text(base_url=self.url)
        self.text_PO2 = Text(base_url=self.url)
        self.projectName = project_name()
        self.textContent = text_Content()
        # self.text_PO.open()
        thread_open([self.text_PO, self.text_PO2])

    def tearDown(self) -> None:
        public_tearDown([self.text_PO, self.text_PO2], self.url, self.home_url, self.username, self.password)
        self.text_PO.driver.quit()

    def test_addAndSync(self):
        '''添加多个文本，输入内容，点击画布同步，再刷新'''
        num = 3
        public_init(self.text_PO, self.username, self.password, self.projectName)
        public_textAdd(self.text_PO, self.textContent, num=num)
        self.text_PO.driver.refresh()
        self.assertTrue(public_check(self.text_PO, self.text_PO.tool_loc))
        text = get_text(self.text_PO, self.text_PO.el_textInput_loc)
        self.assertEqual(text, self.textContent)
        self.assertEqual(num, public_check(self.text_PO, self.text_PO.el_text_loc, islen=True))

    def test_cooperation(self):
        '''协作，编辑锁定'''
        cooperation([self.text_PO, self.text_PO2])
        public_textAdd(self.text_PO, self.textContent)
        double_click(self.text_PO, self.text_PO.el_text_loc)
        self.assertTrue(public_check(self.text_PO2, self.text_PO.el_text_locked))
        bgColor = public_getCSS(self.text_PO2, self.text_PO2.el_text_locked, 'background-color')[0]
        self.assertEqual(bgColor, 'rgba(137, 140, 144, 0.7)')
        self.text_PO2.driver.refresh()
        self.assertTrue(public_check(self.text_PO2, self.text_PO.el_text_locked))
        left_click(self.text_PO, type='sync')
        self.assertFalse(public_check(self.text_PO2, self.text_PO.el_text_locked))

    def addAndDel(self, num):
        #添加文本,若成功，添加内容
        # public_addTool(self.text_PO, self.text_PO.tool_text_loc, self.text_PO.el_text_loc, num=num)
        ws_add(self.text_PO, [('t', num)], text='')
        #是否新建成功
        self.assertEqual(public_check(self.text_PO, self.text_PO.el_text_loc, islen=True), num)
        sleep(3)
        public_revoke_recovery(self.text_PO, self.text_PO.el_text_loc, step=num)  #撤销，恢复
        public_textInput(self.text_PO, self.textContent)  #点击文本，再输入文本
        #点击画布
        left_click(self.text_PO, 100, 80, self.text_PO.header_loc)
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_textInput_loc, self.textContent))
        public_revoke_recovery(self.text_PO, type='input', step=num)
        # self.text_PO.driver.refresh()
        #刷新页面数据是否还在
        # self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNoteText_loc, self.textContent))
        if num > 1:
            selection(self.text_PO, self.text_PO.el_text_loc)  #多选
        rightClick(self.text_PO, el=self.text_PO.el_text_loc, action=self.text_PO.menu_del_loc)
        #是否删除成功
        self.assertFalse(public_check(self.text_PO, self.text_PO.el_text_loc))
        public_revoke_recovery(self.text_PO, self.text_PO.el_text_loc, type='del')
        # click_trash(self.text_PO)  #打开废纸篓进行恢复
        # recovery(self.text_PO)
        #是否恢复成功
        # self.assertTrue(public_check(self.text_PO, self.text_PO.el_text_loc))
        #恢复后的数据是否还在
        # self.assertTrue(public_check(self.text_PO, self.text_PO.el_textNoteText_loc, self.textContent))

    def tes1t_addAndDel(self):
        '''添加文本,若成功，添加内容,然后删除再恢复'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
        self.addAndDel(1)

    def tes1t_ty_addAndDel(self):
        '''体验模式-添加文本,若成功，添加内容,然后删除再恢复'''
        tiyan(self.text_PO)
        self.addAndDel(1)

    def tes1t_multiaddAndDel(self):
        '''多选删除,恢复'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
        self.addAndDel(2)

    def tes1t_ty_muladdAndDel(self):
        '''体验模式-多选删除,恢复'''
        tiyan(self.text_PO)
        self.addAndDel(2)

    def cut(self, num):
        #剪切，粘贴
        # public_addTool(self.text_PO, self.text_PO.tool_text_loc, self.text_PO.el_text_loc, num=num)
        ws_add(self.text_PO, [('t', num)])
        self.assertEqual(public_check(self.text_PO, self.text_PO.el_text_loc, islen=True), num)
        public_textInput(self.text_PO, self.textContent)  #点击文本，再输入文本
        poi_src = public_getElPoi(self.text_PO, self.text_PO.el_text_loc)
        if num > 1:
            selection(self.text_PO, self.text_PO.el_text_loc)  #多选
        rightClick(self.text_PO, el=self.text_PO.el_text_loc, action=self.text_PO.menu_cut_loc)
        #检查是否剪切成功
        self.assertFalse(public_check(self.text_PO, self.text_PO.el_text_loc))
        left_click(self.text_PO, 500, 200, self.text_PO.header_loc)
        #剪切成功后左键点击画布，检查是否有出现元素（BUG点）
        self.assertEqual(public_check(self.text_PO, self.text_PO.el_divs_loc, islen=True), 0)
        rightClick(self.text_PO, action=self.text_PO.menu_paste_loc)
        self.assertEqual(public_check(self.text_PO, self.text_PO.el_text_loc, islen=True), num)
        poi_dst = public_getElPoi(self.text_PO, self.text_PO.el_text_loc)
        public_revoke_recovery(self.text_PO, self.text_PO.el_text_loc, type='cut', poi_src=poi_src, poi_dst=poi_dst)

    def test_cut(self):
        '''剪切，粘贴'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
        self.cut(1)

    def tes1t_ty_cut(self):
        '''体验模式-剪切，粘贴'''
        tiyan(self.text_PO)
        self.cut(1)

    def test_multicut(self):
        '''多选剪切，粘贴'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
        self.cut(2)
        public_delProject(self.text_PO, self.home_url)

    def tes1t_ty_multicut(self):
        '''体验模式-多选剪切，粘贴'''
        tiyan(self.text_PO)
        self.cut(2)

    def tes1t_drag(self):
        '''拖动到文件夹内'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
        # public_addTool(self.text_PO, self.text_PO.tool_text_loc, self.text_PO.el_text_loc)
        ws_add(self.text_PO, [('t', 1)])
        #是否新建成功
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_text_loc))
        public_textInput(self.text_PO, self.textContent)  #点击文本，再输入文本
        #添加文件夹
        public_addTool(self.text_PO, self.text_PO.tool_folder_loc, self.text_PO.el_folder_loc, x=300, y=500)
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_folder_loc))
        #拖动文本到文件夹内
        elDrag(self.text_PO, self.text_PO.el_text_loc, self.text_PO.el_folder_loc)
        # self.assertFalse(public_check(self.text_PO,self.text_PO.el_text_loc))

        public_delProject(self.text_PO, self.home_url)

    def copy(self, num):
        #复制/粘贴
        public_init(self.text_PO, self.username, self.password, self.projectName)
        # public_addTool(self.text_PO, self.text_PO.tool_text_loc, self.text_PO.el_text_loc, num=num)
        ws_add(self.text_PO, [('t', num)])
        #是否新建成功
        self.assertEqual(num, public_check(self.text_PO, self.text_PO.el_text_loc, islen=True))
        if num > 1:
            selection(self.text_PO, self.text_PO.el_text_loc)
        #右键-复制
        rightClick(self.text_PO, el=self.text_PO.el_text_loc, action=self.text_PO.menu_copy_loc)
        #右键-粘贴
        rightClick(self.text_PO, 600, 100, self.text_PO.header_loc, self.text_PO.menu_paste_loc)
        self.assertEqual(public_check(self.text_PO, self.text_PO.el_text_loc, islen=True), num * 2)
        public_revoke_recovery(self.text_PO, self.text_PO.el_text_loc, type='copy', num=num)

    def test_copy(self):
        '''复制/粘贴'''
        self.copy(1)

    def test_multiCopy(self):
        '''多选，复制/粘贴'''
        self.copy(2)

    def cross_copy(self, num):
        public_init(self.text_PO, self.username, self.password, self.projectName)
        self.text_PO.driver.get(self.home_url)
        public_createProject(self.text_PO, '[copy]' + self.projectName[3:].replace(' ', ''))
        public_intoProject(self.text_PO)
        self.assertTrue(public_check(self.text_PO, self.text_PO.tool_loc))
        rightClick(self.text_PO, 200, 100, self.text_PO.header_loc, self.text_PO.menu_paste_loc)
        self.assertEqual(public_check(self.text_PO, self.text_PO.el_text_loc, islen=True), num)
        public_revoke_recovery(self.text_PO, self.text_PO.el_text_loc)

        public_delProject(self.text_PO, self.home_url)

    def tes1t_setBgColor(self):
        '''设置文本背景色,判断颜色设置是否正确'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
        # public_addTool(self.text_PO, self.text_PO.tool_text_loc, self.text_PO.el_text_loc, num=1)
        ws_add(self.text_PO, [('t', 1)], text='')
        #是否新建成功
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_text_loc))
        public_textInput(self.text_PO, self.textContent)
        for i in range(1, 9):
            rightClick(self.text_PO, el=self.text_PO.el_text_loc)  #右键点击
            self.text_PO.text_bgColor(i, self.textContent)
            sleep(1)

    def test_richTextTool(self):
        '''富文本工具栏位置检查'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
        #文本位于顶部位置，富文本工具栏在其下方显示
        # public_addTool(self.text_PO, self.text_PO.tool_text_loc, self.text_PO.el_text_loc, y=130)
        ws_add(self.text_PO, [('t', 1)], text='')
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_text_loc))
        public_textInput(self.text_PO, self.textContent)
        double_click(self.text_PO, self.text_PO.el_text_loc)
        poi_text_tool = public_getElPoi(self.text_PO, self.text_PO.richText_tool)
        self.assertTrue(poi_text_tool[0]['y'] > 190)
        self.text_PO.driver.refresh()
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_text_loc))
        rightClick(self.text_PO, self.text_PO.el_text_loc, action=self.text_PO.menu_del_loc)
        #文本位于底部位置，富文本工具栏在其上方显示
        # public_addTool(self.text_PO, self.text_PO.tool_text_loc, self.text_PO.el_text_loc, y=800)
        ws_add(self.text_PO, [('t', 1)], text='', y=800)
        double_click(self.text_PO, self.text_PO.el_text_loc)
        poi_text_tool = public_getElPoi(self.text_PO, self.text_PO.richText_tool)
        self.assertTrue(poi_text_tool[0]['y'] < 760)
        left_click(self.text_PO, 100, 100, self.text_PO.header_loc)

    def test_check_richTextTool(self):
        '''检查富文本工具栏是否正常显示'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
        ws_add(self.text_PO, [('t', 1), ('i', 1)], margin=200)
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_text_loc))
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_imgDIV_loc))
        #先双击文本，再单击画布，再双击文本
        double_click(self.text_PO, self.text_PO.el_text_loc)
        self.assertTrue(public_check(self.text_PO, self.text_PO.richText_tool))
        left_click(self.text_PO, 100, 100, self.text_PO.header_loc)
        double_click(self.text_PO, self.text_PO.el_text_loc)
        self.assertTrue(public_check(self.text_PO, self.text_PO.richText_tool))
        #点击其它元素，再双击文本
        el_click(self.text_PO, self.text_PO.el_imgDIV_loc)
        double_click(self.text_PO, self.text_PO.el_text_loc)
        self.assertTrue(public_check(self.text_PO, self.text_PO.richText_tool))
        #再添加一个文本，两个文本顺序双击
        ws_add(self.text_PO, [('t', 1)], x=600, y=200)
        self.assertEqual(public_check(self.text_PO, self.text_PO.el_text_loc, islen=True), 2)
        self.text_PO.check_richTextTool()

    def test_posi(self):
        '''检查刷新页面后屏幕是否会自动定位到最后编辑的元素'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
        ws_add(self.text_PO, [('t', 1)])
        ws_add(self.text_PO, [('t', 1)], x=2500, y=1500, text='position')
        self.assertEqual(public_check(self.text_PO, self.text_PO.el_text_loc, islen=True), 2)
        self.text_PO.check_posi()
        self.text_PO.driver.refresh()
        self.assertTrue(public_check(self.text_PO, self.text_PO.el_text_loc))
        scroll = public_getScrollPosi(self.text_PO)
        print('scroll:{0}'.format(scroll))
        self.assertTrue(scroll['top'] > 900)
        self.assertTrue(scroll['left'] > 1500)

    def test_rich_fontFamily(self):
        '''富文本-字体'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
        public_textAdd(self.text_PO, '666666')
        self.text_PO.check_rich_font(self.text_PO.rich_fontFamily_loc)

    def test_rich_fontSize(self):
        '''富文本-字号'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
        public_textAdd(self.text_PO, '666666')
        self.text_PO.check_rich_font(self.text_PO.rich_fontSize_loc)

    def test_rich_fontStyle(self):
        '''富文本-加粗，斜体，下划线。加粗bug（要撤销两次）'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
        public_login(self.text_PO2, self.username2, self.password)
        join_invite([self.text_PO, self.text_PO2])
        public_textAdd(self.text_PO, '666666')
        #富文本-加粗,bug（要撤销两次）
        self.text_PO.check_rich_fontStyle(self.text_PO.rich_B_loc, 'font-weight', '700')
        self.text_PO2.check_text_asyn('fontStyle', style='font-weight', value='700')
        do_revoke(self.text_PO, step=2)
        self.assertFalse(public_check(self.text_PO, self.text_PO.el_textSpan_loc))
        #富文本-斜体
        self.text_PO.check_rich_fontStyle(self.text_PO.rich_italic_loc, 'fontStyle', 'italic')
        self.text_PO2.check_text_asyn('fontStyle', style='fontStyle', value='italic')
        do_revoke(self.text_PO)
        self.assertFalse(public_check(self.text_PO, self.text_PO.el_textSpan_loc))
        #富文本-下划线
        self.text_PO.check_rich_fontStyle(self.text_PO.rich_underline_loc, 'textDecorationLine', 'underline')
        self.text_PO2.check_text_asyn('fontStyle', style='textDecorationLine', value='underline')
        do_revoke(self.text_PO)
        self.assertFalse(public_check(self.text_PO, self.text_PO.el_textSpan_loc))

    def test_rich_fontColor(self):
        '''富文本-字体颜色'''
        public_init(self.text_PO, self.username, self.password, self.projectName)
        public_textAdd(self.text_PO, '666666')
        self.text_PO.check_rich_font(self.text_PO.rich_fontColor_loc)

    def test_rich_textAlign(self):
        '''富文本-对齐方式'''
        cooperation([self.text_PO, self.text_PO2])
        public_textAdd(self.text_PO, '666666')
        #富文本-居中
        self.text_PO.check_rich_align(self.text_PO.rich_centerA_loc, 'center')
        self.text_PO2.check_text_asyn('align', value='center')
        #富文本-右对齐
        self.text_PO.check_rich_align(self.text_PO.rich_rightA_loc, 'right')
        self.text_PO2.check_text_asyn('align', value='right')
        #富文本-左对齐
        self.text_PO.check_rich_align(self.text_PO.rich_leftA_loc, 'left')
        self.text_PO2.check_text_asyn('align', value='left')

    def test_rich_sort(self):
        '''富文本-有序无序'''
        cooperation([self.text_PO, self.text_PO2])
        text = '666666'
        public_textAdd(self.text_PO, text)
        #富文本-无序列表
        self.text_PO.check_rich_sort(self.text_PO.rich_sortDisorder_loc, text)
        self.text_PO2.check_text_asyn('sort', el=self.text_PO2.el_text_ulsort)
        #富文本-有序列表
        self.text_PO.check_rich_sort(self.text_PO.rich_sortOrder_loc, text)
        self.text_PO2.check_text_asyn('sort', el=self.text_PO2.el_text_olsort)

    def te1st_input(self):
        public_init(self.text_PO, self.username, self.password, self.projectName)
        self.text_PO.find_element(*self.text_PO.tool_text_loc).click()
        sleep(1)
        left_click(self.text_PO, 300, 150, self.text_PO.header_loc)
        self.text_PO.find_element(*self.text_PO.el_textInput_loc).send_keys(self.textContent)


if __name__ == "__main__":
    # unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(TextTest('test_rich_sort'))
    unittest.TextTestRunner().run(suite)
