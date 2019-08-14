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
    passwd = get_locater('LoginPage', 'passwd')
    check_text = get_locater('LoginPage', 'check_text')
    submit_button = get_locater('LoginPage', 'submit_button')
    user_name = get_locater('LoginPage', 'user_name')

    
class AddSelfBoard:
    dialog_title = get_locater('AddSelfBoard', 'dialog_title')

    
class DataBoard:
    self_station_type_arrow = get_locater('DataBoard', 'self_station_type_arrow')
    self_station_type = get_locater('DataBoard', 'self_station_type')
    add_self_board = get_locater('DataBoard', 'add_self_board')
    tab_self_data = get_locater('DataBoard', 'tab_self_data')

    
class NavBar:
    data_board = get_locater('NavBar', 'data_board')
    tool_arrow = get_locater('NavBar', 'tool_arrow')

    

