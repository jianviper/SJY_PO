#!/usr/bin/env python
#coding:utf-8

class PizzaFactory(object):
    # 定义一个createPizza方法，所有客户都使用这个方法来实例化新对象
    def createPizza(self, name):
        #选择哪款pizza
        if name == 'c':
            self.pizza = CheesePizza()
        elif name == 'g':
            self.pizza = GreekPizza()
        elif name == 'p':
            self.pizza = PepperoniPizza()
        #返回一个pizza实例
        return self.pizza


#开了家店
class PizzaStore(object):

    def __init__(self):
        self.factory = PizzaFactory()

    def orderPizze(self, name):
        #通过工厂的createPizza方法，返回需要的披萨实例
        self.pizza = self.factory.createPizza(name)
        return self.pizza

        # print(self.pizza.prepare())
        # print(self.pizza.bake())
        # print(self.pizza.cut())
        # print(self.pizza.box())


#目前只有一种披萨可以定
class Pizza(object):
    def prepare(self):
        return "prepare pizza"

    def bake(self):
        return "bake pizza"

    def cut(self):
        return "cut pizza"

    def box(self):
        return "box pizza"


#------------扩展了多种pizza------------
class CheesePizza(object):  #第一种pizza
    def prepare(self):
        return "prepare Cheese pizza"

    def bake(self):
        return "bake Cheese pizza"

    def cut(self):
        return "cut Cheese pizza"

    def box(self):
        return "box Cheese pizza"


class GreekPizza(object):  #第二种pizza
    def prepare(self):
        return "prepare Greek pizza"

    def bake(self):
        return "bake Greek pizza"

    def cut(self):
        return "cut Greek pizza"

    def box(self):
        return "box Greek pizza"


class PepperoniPizza(object):  #第三种pizza
    def prepare(self):
        return "prepare Pepperoni pizza"

    def bake(self):
        return "bake Pepperoni pizza"

    def cut(self):
        return "cut Pepperoni pizza"

    def box(self):
        return "box Pepperoni pizza"


if __name__ == '__main__':
    pizze = PizzaStore().orderPizze('c')
    print(pizze)
