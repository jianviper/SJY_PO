#!/usr/bin/env python
#coding:utf-8
import abc


class Bmw(object):
    def __repr__(self):
        return 'bmw'


class Benz(object):
    def __repr__(self):
        return 'benz'


#小轿车
class Benz_c200(object):
    def __repr__(self):
        return 'benz_c200'


class Bmw_3s(object):
    def __repr__(self):
        return 'bmw_3'


#suv
class Benz_glc(object):
    def __repr__(self):
        return 'benz_glc'


class Bmw_x5(object):
    def __repr__(self):
        return 'bmw_x5'


class CarFactory(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def product_car(self):
        pass

    @abc.abstractmethod
    def product_suv(self):
        pass


class BmwFactory(CarFactory):

    @classmethod
    def product_car(self):
        return Bmw_3s()

    @classmethod
    def product_suv(self):
        return Bmw_x5()


class BenzFactory(CarFactory):

    @classmethod
    def product_car(self):
        return Benz_c200()

    @classmethod
    def product_suv(self):
        return Benz_glc()


if __name__ == '__main__':
    c1 = BmwFactory.product_car()
    c2 = BenzFactory.product_car()
    print(c1, c2)
    s1 = BmwFactory.product_suv()
    s2 = BenzFactory.product_suv()
    print(s1, s2)
