# coding:utf-8

import configparser
from os import path

current = path.dirname(__file__)
root = path.dirname(current)
cfg_file_path = root + '/runningplan/cfgfile/'


class ReadCfgFile(object):
    def __init__(self, file_name='cfg.ini', dir_name='api'):
        cfg_file = cfg_file_path + dir_name + '/' + file_name
        self.cf = configparser.ConfigParser()
        self.cf.read(cfg_file, encoding='utf-8')

    def get_val(self, section, option):
        value = self.cf.get(section, option)
        return value

    def get_options(self, section):
        option = self.cf.options(section)
        return option

    def get_items(self, section):
        items = self.cf.items(section)
        return items





