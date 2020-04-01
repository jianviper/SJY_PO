#!/usr/bin/env python
#coding:utf-8
from random import randint

def buildPosition(x,y,height,width):
    pX=randint(-x,width-x)
    pY=randint(280-y,height-100)