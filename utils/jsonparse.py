# coding:utf-8
from jsonpath_rw_ext import parse


def parser(json_data, json_path):
    '''
    pls note that the returned result is a list.
    '''
    result = [match.value for match in parse(json_path).find(json_data)]
    return result



