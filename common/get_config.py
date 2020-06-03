#!/usr/bin/env python
#coding:utf-8
import configparser, os


def get_url():
    config = configparser.ConfigParser()
    file_name = 'config.ini'
    dir = os.getcwd().split('\\')
    if dir[-2] == 'SJY_PO':
        file_name = '../config.ini'
    config.read(file_name)
    return [config.get('host', 'url'), config.get('host', 'home_url')]
    # print(config.sections())
    #
    # print(config.options('host'))
    #
    # print(config.items('host'))
    #
    # print(config.get('host', 'url'))


if __name__ == '__main__':
    print(get_url())
