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


def get_url():  #生成登录url和home页url
    config = config_read()
    login_url = 'https://{1}.bimuyu.tech/login'
    home_url = 'https://{1}.bimuyu.tech/home'
    host = config.get('host', 'host')
    return [login_url.format('', host), home_url.format('', host)]
    # print(config.sections())
    #
    # print(config.options('host'))
    #
    # print(config.items('host'))
    #
    # print(config.get('host', 'url'))


def get_ws():  #生成websocket链接地址前缀
    config = config_read()
    host = config.get('host', 'host')
    if host == 'app': host = 'api'
    return 'wss://{0}.bimuyu.tech/api/echo'.format(host)


def get(section, item):
    config = config_read()
    return config.get(section, item)


if __name__ == '__main__':
    print(get_ws())
    print(get('folder', 'icon'))
