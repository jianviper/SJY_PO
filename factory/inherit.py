#!/usr/bin/env python
#coding:utf-8


class Parent1(object):

    def __init__(self):
        self.name = 'linda'

    def say(self, name):
        print('my name is {0}'.format((name, self.name)))


class Child1(Parent1):

    def say(self, **kwargs):
        super(Child1, self).say('dalin')
        print('my name is small')


class Parent2:
    def __init__(self):
        print('This is parent init.')

    def sleep(self):
        print("Parent sleeps.")


class Child2(Parent2):
    def __init__(self):
        Parent2.__init__(self)
        print('This is child init.')

    def sleep(self):
        print("Child sleeps.")


class Parent:
    def __init__(self):
        print('This is parent init.')

    def sleep(self, time):
        print("Parent sleeps {0}sec.".format(time))


class Child(Parent):
    def __init__(self):
        #Parent.__init__(self)
        super().__init__()
        print('This is child init.')

    def sleep(self, **kwargs):
        print("Child sleeps.")


if __name__ == '__main__':
    c = Child()
    c.sleep()
    super(Child, c).sleep(20)
