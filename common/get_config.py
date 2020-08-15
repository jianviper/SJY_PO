#!/usr/bin/env python
#coding:utf-8
import configparser, os


def config_read():
    config = configparser.ConfigParser()
    file_name = 'config.ini'
    dir = os.getcwd().split('\\')
    if dir[-2] == 'SJY_PO': file_name = '../config.ini'
    config.read(file_name, encoding='utf-8')
    return config


def get_url():
    config = config_read()
    return [config.get('host', 'url'), config.get('host', 'home_url')]
    # print(config.sections())
    #
    # print(config.options('host'))
    #
    # print(config.items('host'))
    #
    # print(config.get('host', 'url'))


def get(section, item):
    config = config_read()
    return config.get(section, item)


if __name__ == '__main__':
    print(get_url())
    print(get('folder', 'src'))
