# coding=utf-8
import yaml
import os
import os.path
from inspect import getsourcefile

current_dir = os.path.dirname(os.path.abspath(getsourcefile(lambda: 0)))
dir_name = os.path.basename(current_dir)
par_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
par_par_dir = str(os.path.abspath(os.path.join(par_dir, os.path.pardir)))
yaml_path = par_par_dir + '/yaml/' + dir_name + '/'


def parser(yaml_path):
    pages = {}
    for root, dirs, files in os.walk(yaml_path):
        for name in files:
            watch_file_path = os.path.join(root, name)
            with open(watch_file_path, 'r', encoding='utf-8') as f:
                page = yaml.safe_load(f)
            pages.update(page)
    return pages


def get_locater(clazz_name, method_name):
    pages = parser(yaml_path)
    locators = pages[clazz_name]['locators']
    for locator in locators:
        if locator['name'] == method_name:
            return locator['type'] + '=>' + locator['value']


class LoginPage:
    # 登录页面，页面元素获取
    user_name = get_locater('LoginPage', 'user_name')
    passwd = get_locater('LoginPage', 'passwd')
    submit_button = get_locater('LoginPage', 'submit_button')

    
class NavBar:
    # 左侧导航栏，页面元素获取
    cim_act = get_locater('NavBar', 'cim_act')
    act_device = get_locater('NavBar', 'act_device')

    
class DevicePage:
    # 设备页面，页面元素获取
    iframe_device = get_locater('DevicePage', 'iframe_device')
    device_menu_tab = get_locater('DevicePage', 'page_title')
    park_selector = get_locater('DevicePage', 'park_selector')
    select_park05 = get_locater('DevicePage', 'select_park05')
    seach_system = get_locater('DevicePage', 'seach_system')
    device_code01 = get_locater('DevicePage', 'device_code01')

    add_device = get_locater('DevicePage', 'add_device')
    add_device_name = get_locater('DevicePage', 'add_device_name')
