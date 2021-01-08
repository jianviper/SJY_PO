#!/usr/bin/env python
#coding:utf-8
import json
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from common.ws_client import add_ws, ws_creat
from time import sleep, strftime
from .fc_tool_page import PageTool


class WorkerTool():

    def __init__(self, PO):
        self.PO = PO
        self.header_loc = (By.CLASS_NAME, 'header_fix')

    def getElSize(self, el):  #获取元素的尺寸
        '''{"height":100,"width":200}'''
        p_list = []
        if self.PO.find_elements(*el):
            for e in self.PO.find_elements(*el):
                p_list.append(e.size)
            return p_list

    def getElPoi(self, el, **kwargs):  #获取元素位置
        '''{"x":222,"y":333}'''
        if kwargs.get('driver'):
            find = self.PO.driver.find_elements_by_css_selector(el)
        else:
            find = self.PO.find_elements(*el)
        if find:
            poi_list = []
            for e in find:
                poi_list.append(e.location)
            return poi_list

    def getAttrs(self, el, attr_name):
        if self.PO.find_element(*el):
            idList = []
            for e in self.PO.find_elements(*el):
                id = e.get_attribute(attr_name)
                idList.append(id)
            return idList

    def public_getScrollPosi(self):
        #获取滚动条的位置
        top_js = 'return document.documentElement.scrollTop;'
        left_js = 'return document.documentElement.scrollLeft;'
        top = self.PO.driver.execute_script(top_js)
        left = self.PO.driver.execute_script(left_js)
        return {'top': top, 'left': left}

    def getCss(self, el, css_name):
        css = []
        for e in self.PO.find_elements(*el):
            c = e.value_of_css_property(css_name)
            css.append(c)
        if len(css) == 1:
            return css[0]
        return css

    def _getSelectPoi(self, el):
        #获取设置指定元素的选取范围
        x, y = [], []
        if type(el) == list and len(el) > 0:
            for e in el:
                if self.PO.find_element(*e):
                    for ee in self.PO.find_elements(*e):
                        x.append(ee.location['x'])
                        y.append(ee.location['y'])
        else:
            if self.PO.find_element(*el):
                for ee in self.PO.find_elements(*el):
                    x.append(ee.location['x'])
                    y.append(ee.location['y'])
        # print('*****\r\n', x, y, '\r\n*******\r\n')
        return ((min(x) - 20, min(y) - 20), (max(x) + 20, max(y) + 20))
        # return (self.PO.find_element(*el).location, self.PO.find_element(*el).location_once_scrolled_into_view)

    def selection(self, el):
        '''
        根据需求多选元素
        :param PO:
        :param el: 要选择的元素，可以是列表
        :return:
        '''
        sleep(1)
        action = ActionChains(self.PO.driver)
        SP = self._getSelectPoi(el)
        print("selectPoi:{0}".format(SP))
        action.move_to_element_with_offset(self.PO.find_element(*self.header_loc), SP[0][0], SP[0][1])
        action.click_and_hold()
        action.move_to_element_with_offset(self.PO.find_element(*self.header_loc), SP[1][0], SP[1][1])
        action.release().perform()
        sleep(1)

    def tool_add(self, toolEL, checkEL, num=1, **kwargs):
        '''
        登录，新建项目，进入项目添加工具
        :param PO:
        :param toolEL: 左侧工具栏的工具按钮
        :param checkEL: 添加后生成的元素
        :param num: 添加的元素数量
        :param kwargs: 可传参数x，y设置初始位置
        :return:
        '''
        height, margin = 0, 0
        x, y = kwargs.get('x', 200), kwargs.get('y', 150)  #初始位置
        for i in range(num):
            self.PO.find_element(*toolEL).click()
            if i > 0:  #添加了一个元素之后
                size = self.getElSize(checkEL)[i - 1]
                height, margin = size['height'], 50
            self.left_click(x, y + (height + margin) * i, self.header_loc)
            #检查是否新建成功
            if toolEL == (By.CSS_SELECTOR, '.work_tool>div:nth-child(5)'):
                assert bool(self.PO.find_element(*(By.CLASS_NAME, 'work_text_tool'))) == True
            elif toolEL == (By.CSS_SELECTOR, '.work_tool>div:nth-child(6)'):
                assert bool(self.PO.find_element(*(By.CLASS_NAME, 'work_note_tool'))) == True
            sleep(1)
            self.left_click(50, 100, self.header_loc)

    def text_add(self, text=None, num=1, **kwargs):
        x, y = kwargs.get('x', 200), kwargs.get('y', 130)
        jss = '''
                        var ds=document.getElementsByClassName('text_content'); 
                        for(i=0;i<ds.length;i++){
                            console.log(ds[i]);
                            ds[i].parentNode.style.border='3px solid red';
                            console.log(ds[i].innerText.length);
                            if (ds[i].innerText.length<1){
                                 ds[i].innerText="%s";   
                                }
                        }
                        ''' % text
        self.PO.find_element(*(By.CSS_SELECTOR, '.work_tool>div:nth-child(5)')).click()
        sleep(1)
        self.left_click(x, y, self.header_loc)
        for i in range(num):
            if i > 0:
                self.left_click(x, y + 70 * i, self.header_loc)
                self.double_click()
            sleep(1)
            # self.PO.driver.execute_script(jss)
            if text:
                self.PO.find_elements(*(By.CLASS_NAME, 'text_content'))[0].send_keys(text)
            else:
                self.PO.find_elements(*(By.CLASS_NAME, 'text_content'))[0].send_keys(
                    PageTool(self.PO).textNote_Content())
            self.left_click(100, 100, self.header_loc)
            sleep(1)

    def note_add(self, text=None, num=1, **kwargs):
        '''
            通过工具栏添加便签
            :param PO:
            :param text: 文本内容
            :param num: 数量
            :param kwargs: 可传x，y初始坐标
            :return:
        '''
        x, y = kwargs.get('x', 200), kwargs.get('y', 130)
        self.PO.find_element(*(By.CSS_SELECTOR, '.work_tool>div:nth-child(6)')).click()
        sleep(1)
        self.left_click(x, y, self.header_loc)
        for i in range(num):
            if i > 0:
                self.left_click(x, y + 240 * i, self.header_loc)
                self.double_click()
            sleep(1)
            if text:
                self.PO.find_element(*(By.CLASS_NAME, 'item_t_bg')).click()
                self.PO.find_elements(*(By.CLASS_NAME, 'text_content'))[i].send_keys(text)
            self.left_click(100, 100, self.header_loc)
            sleep(1)

    def ws_add(self, els, **kwargs):
        '''
        通过websocket添加元素
        :param PO:
        :param els: 需要添加的元素，格式:[("t",1),("i",2),("f",2)]
        t:文本便签，i：图片便签，f：文件夹，file：文件
        :param kwargs: 可传入x，y设置初始位置
        :return:
        '''
        x, y = kwargs.get('x', 200), kwargs.get('y', 150)  #初始位置
        margin = kwargs.get('margin', 50)  #元素之间的垂直距离
        type, ws = None, None
        if els == 'all':
            els = [('t', 1), ('n', 1), ('i', 1), ('f', 1)]
        try:
            ws = ws_creat(self.PO)
            for el in els:  #格式els:[("t",1),("i",2),("f",2)]
                el_y_margin = 0
                #根据类型设置ws请求类型和元素高度
                if el[0] == "t":
                    type = "TEXT_LABEL_ADD"
                    el_y_margin = 60
                elif el[0] == "n":
                    type = "NOTE_LABEL_ADD"
                    el_y_margin = 200
                elif el[0] == "i":
                    type = "IMAGE_LABEL_ADD"
                    el_y_margin = 150
                elif el[0] == 'f':
                    type = "CANVAS_ADD"
                    el_y_margin = 100
                elif el[0] == 'file':
                    type = 'FILE_LABEL_ADD'
                    el_y_margin = 990
                    if len(el) == 3 and (el[2] == 'ppt' or el[2] == 'excel'):
                        el_y_margin = 480
                for i in range(el[1]):
                    utime = strftime('%Y-%m-%d %H:%M:%S')
                    content = 'AutoTestContent-{0}'.format(utime)
                    add_ws(self.PO, type, x, y, ws=ws, text=kwargs.get('text', content))  #请求websocket
                    y = y + el_y_margin + margin
                    sleep(1)
            self.PO.driver.refresh()
        except BaseException as e:
            print(e)
        finally:
            if ws:
                print('websocket is closing...')
                ws.close()

    def left_click(self, x=0, y=0, el=None, type=None):
        '''
        左键点击，可以指定元素及相对位置进行
        :param PO:
        :param x: x偏移量
        :param y: y偏移量
        :param el: 在哪个元素上左键点击
        :return:
        '''
        # print('x:{0},y:{1}'.format(x, y))
        action = ActionChains(self.PO.driver)
        if type == 'sync': x, y, el = 80, 80, self.header_loc
        if x and y and el:  #在指定元素的相对位置
            action.move_to_element_with_offset(self.PO.find_element(*el), x, y).click().perform()
        elif x and y:  #在当前鼠标位置的相对偏移位置
            action.move_by_offset(x, y).click().perform()
        elif el:  #在指定元素上
            action.click(self.PO.find_element(*el)).perform()
        sleep(1.5)

    def rightClick(self, x=0, y=0, el=None, action=None):
        '''
        右键点击,可以指定元素及其相对位置，也可右键菜单操作
        :param PO:
        :param x: x偏移量
        :param y: y偏移量
        :param el: 在哪个元素上右键点击
        :param action: 右键菜单的选项
        :return:
        '''
        actionC = ActionChains(self.PO.driver)
        if x and y and el:  #在指定元素的相对位置
            if el == (By.CLASS_NAME, 'menu_item'):
                x = 700
            actionC.move_to_element_with_offset(self.PO.find_element(*el), x, y).context_click().perform()
        elif el:  #在指定元素上
            actionC.context_click(self.PO.find_element(*el)).perform()
        else:  #在鼠标当前位置
            actionC.context_click().perform()
        sleep(1.0)
        if action:
            self.PO.find_element(*action).click()
            sleep(1.5)

    def double_click(self, el=None):
        #双击元素
        sleep(1)
        action = ActionChains(self.PO.driver)
        if el and self.PO.find_element(*el):
            action.double_click(self.PO.find_element(*el)).perform()
        else:
            action.double_click().perform()

    def click_trash(self, PO):  #打开废纸篓
        tool_recovery_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(9)')
        tips_loc = (By.CLASS_NAME, 'ant-notification-close-x')
        if self.PO.find_element(*tips_loc, waitsec=2):
            self.PO.driver.refresh()
        self.PO.find_element(*tool_recovery_loc).click()

    def recovery(self, PO):
        '''恢复删除的元素'''
        el_trashEL_loc = (By.CSS_SELECTOR, '.item_list>li')
        tool_mouse_loc = (By.CSS_SELECTOR, '.work_tool>div:nth-child(1)')

        if self.PO.find_elements(*el_trashEL_loc):
            for el in self.PO.find_elements(*el_trashEL_loc):
                el.click()
                sleep(0.5)
        self.PO.find_element(*tool_mouse_loc).click()

    def elDrag(self, el=None, start=None, end=None, PO=None):
        '''
        按住某个元素拖动，根据el决定是否拖动到空白处还是某个元素上
        :param PO:
        :param el: 指定从这个元素上拉出关联线
        :param start: 开始元素，有传el代表offset_x
        :param end: 结束元素，有传el代表offset_y
        :return:
        '''
        sleep(1)
        action = ActionChains(self.PO.driver)
        if PO:
            action = ActionChains(PO.driver)
        if el:
            self.PO.find_element(*el).click()
            sleep(1)
            action.drag_and_drop_by_offset(self.PO.find_element(*el), start, end).perform()
        else:
            action.drag_and_drop(self.PO.find_element(*start), self.PO.find_element(*end)).perform()
        sleep(1)

    def public_textInput(self, text):
        #文本便签利用JS进行赋值
        js = '''
            document.querySelector('.work_text.work_element').style.border='5px solid red';
            document.getElementsByClassName("text_content")[0].append('{0}');'''.format(text)
        jss = '''
            var ds=document.getElementsByClassName('text_content'); 
            for(i=0;i<ds.length;i++){
                ds[i].parentNode.style.border='3px solid red';
                ds[i].append("%s");
            }
            ''' % text
        self.PO.driver.execute_script(jss)
        if len(self.PO.find_elements(*self.PO.el_textNote_loc)) > 0:
            el_textContent_loc = (By.CSS_SELECTOR, '.work_text.work_element>.text_content')
            action = ActionChains(self.PO.driver)
            for e in self.PO.find_elements(*el_textContent_loc):
                action.double_click(e).perform()
                sleep(1)
                self.left_click(50, 100, self.header_loc)

    def public_Input(self, el, text):
        for e in self.PO.find_elements(*el):
            e.send_keys(text)

    def do_revoke(self, step=1):  #撤销
        ws = None
        try:
            ws = ws_creat(self.PO)
            data = {"type": "REVOKE"}
            for i in range(step):
                ws.send(json.dumps(data))
        except BaseException as e:
            print(e)
        finally:
            if ws: ws.close()
            sleep(1)

    def do_recovery(self, step=1):  #恢复
        ws = None
        try:
            ws = ws_creat(self.PO)
            data = {"type": "RECOVERY"}
            for i in range(step):
                ws.send(json.dumps(data))
        except BaseException as e:
            print(e)
        finally:
            if ws: ws.close()
            sleep(1)

    def public_revoke(self, el=None, **kwargs):
        '''
        撤销，恢复
        :param PO:
        :param el: 被撤销和恢复的元素
        :param kwargs: 可传参数type:操作类型，step:撤销和恢复的步数,num:数量
        :return:
        '''
        if kwargs.get('type') == 'input':  #文本便签的输入
            el_textContent_loc = (By.CSS_SELECTOR, '.work_text.work_element>.text_content')
            self.do_revoke(kwargs.get('step', 1))  #撤销
            for el in self.PO.find_elements(*el_textContent_loc):
                assert el.text == ''
            self.do_recovery(kwargs.get('step', 1))  #恢复
            for el in self.PO.find_elements(*el_textContent_loc):
                assert el.text != ''
        elif kwargs.get('type') == 'del':  #元素删除
            self.do_revoke(kwargs.get('step', 1))
            assert self.PO.find_element(*el) != None
            self.do_recovery(kwargs.get('step', 1))
            assert self.PO.find_element(*el) == None
        elif kwargs.get('type') == 'cut':  #元素剪切
            self.do_revoke(kwargs.get('step', 1))
            if len(kwargs.get('poi_src')) > 1:  #当有多个元素的时候
                poi = self.getElPoi(el, driver=kwargs.get('driver'))
                assert len(kwargs.get('poi_src')) == len(poi)
                for p in poi:
                    assert p in kwargs.get('poi_src')
            else:
                assert self.getElPoi(el, driver=kwargs.get('driver')) == kwargs.get('poi_src')
            self.do_recovery(kwargs.get('step', 1))
            if len(kwargs.get('poi_dst')) > 1:  #当有多个元素的时候
                poi = self.getElPoi(el, driver=kwargs.get('driver'))
                assert len(kwargs.get('poi_dst')) == len(poi)
                for p in poi:
                    assert p in kwargs.get('poi_dst')
            else:
                assert self.getElPoi(el, driver=kwargs.get('driver')) == kwargs.get('poi_dst')
        elif kwargs.get('type') == 'copy':  #元素复制
            self.do_revoke(kwargs.get('step', 1))
            if kwargs.get('driver'):
                assert len(self.PO.driver.find_elements_by_css_selector(el)) == kwargs.get('num', 1)
            else:
                assert len(self.PO.find_elements(*el)) == kwargs.get('num', 1)
            self.do_recovery(kwargs.get('step', 1))
            if kwargs.get('driver'):
                assert len(self.PO.driver.find_elements_by_css_selector(el)) == kwargs.get('num', 1) * 2
            else:
                assert len(self.PO.find_elements(*el)) == kwargs.get('num', 1) * 2
        elif kwargs.get('type') == 'rotate' or kwargs.get('type') == 'origin':
            #图片便签的旋转或原图尺寸
            self.do_revoke()
            assert self.getElSize(el) == kwargs.get('size1')
            self.do_recovery()
            assert self.getElSize(el) == kwargs.get('size2')
        elif kwargs.get('type') == 'cc':  #文件夹修改颜色
            self.do_revoke(kwargs.get('step', 1))
            assert self.getAttrs(el, 'src')[0] == kwargs.get('src')
            self.do_recovery(kwargs.get('step', 1))
            assert self.getAttrs(el, 'src')[0] == kwargs.get('dst')
        else:  #元素添加的撤销和恢复
            self.do_revoke(kwargs.get('step', 1))
            assert self.PO.find_element(*el) == False
            self.do_recovery(kwargs.get('step', 1))
            assert self.PO.find_element(*el) != False

    def elAddLine(self, start=None, end=None):
        '''
        两个元素之间新建关联线
        :param PO:
        :param start: 起始元素的关联线节点
        :param end: 终止元素,已定位
        :return:
        '''
        sleep(1)
        action = ActionChains(self.PO.driver)
        action.drag_and_drop(self.PO.find_element(*start), end).perform()
        sleep(1)

    def addWithLine(self, els, start=None, end=None):
        '''
        添加元素，且加上关联线
        :param PO:
        :param els: 要添加的元素
        :param start: 起始元素
        :param end: 结束元素
        :return:
        '''
        btn_relbtm_loc = (By.CLASS_NAME, 'relation_bottom')
        self.ws_add(els)
        if start and end:  #如果多个不同的元素
            self.PO.find_element(*start).click()
            self.elAddLine(btn_relbtm_loc, self.PO.find_element(*end))
        elif start:  #同一种元素
            el_list = self.PO.find_elements(*start)
            if el_list:
                for i in range(len(el_list)):
                    el_list[0].click()
                    self.elAddLine(btn_relbtm_loc, el_list[1])
            else:
                raise Exception("页面中未找到{0}元素".format(start))
        self.left_click(80, 100, self.header_loc)

    def public_exJS(self, js):
        return self.PO.driver.execute_script(js)
