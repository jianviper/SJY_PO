#!/usr/bin/env python
#coding:utf-8
from parts.fc_tool_worker import WorkerTool


class ElementFactory(object):

    def create_factory(self, name, po):
        ele_factory = None
        if name == 'text':
            ele_factory = TextNote(po)
        return ele_factory


class ElementCreater(object):
    def __init__(self):
        self.factory = ElementFactory()

    def create_element(self, name, po):
        element = self.factory.create_factory(name, po)
        return element


class TextNote(WorkerTool):
    '''文本便签工厂'''

    def __init__(self, PO):
        super().__init__(PO)

    def tool_add(*args, **kwargs):
        print('add textnote')

    @classmethod
    def cm(cls):
        print('classmethod func')


if __name__ == '__main__':
    text = ElementCreater().create_element('text', 'po')
    text.add_textnote()
