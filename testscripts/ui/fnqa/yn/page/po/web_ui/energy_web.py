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


class MyMenuW:
    yn_analyze = get_locater('MyMenuW', 'yn_analyze')
    yesterday_energy_board = get_locater('MyMenuW', 'yesterday_energy_board')
    month_energy_board = get_locater('MyMenuW', 'month_energy_board')
    prod_online = get_locater('MyMenuW', 'prod_online')
    yn_optimization = get_locater('MyMenuW', 'yn_optimization')
    electric_cost_optimization = get_locater('MyMenuW', 'electric_cost_optimization')
    product_consumption = get_locater('MyMenuW', 'product_consumption')
    yn_safe = get_locater('MyMenuW', 'yn_safe')
    addelectric = get_locater('MyMenuW', 'addelectric')
    yn_report_page = get_locater('MyMenuW', 'yn_report_page')
    enterprise_electric = get_locater('MyMenuW', 'enterprise_electric')
    enterprise_steam = get_locater('MyMenuW', 'enterprise_steam')
    power_recall = get_locater('MyMenuW', 'power_recall')
    energy_plan = get_locater('MyMenuW', 'energy_plan')
    yn_productdata = get_locater('MyMenuW', 'yn_productdata')
    production_data = get_locater('MyMenuW', 'production_data')
    productdata_statistics = get_locater('MyMenuW', 'productdata_statistics')
    power_key = get_locater('MyMenuW', 'power_key')

    
class LoginPage:
    user_name = get_locater('LoginPage', 'user_name')
    passwd = get_locater('LoginPage', 'passwd')
    submit_button = get_locater('LoginPage', 'submit_button')
    check_text = get_locater('LoginPage', 'check_text')

    
class EnIndex:
    yn_analyze = get_locater('EnIndex', 'yn_analyze')
    yn_optimization = get_locater('EnIndex', 'yn_optimization')
    yn_safe = get_locater('EnIndex', 'yn_safe')
    yn_report = get_locater('EnIndex', 'yn_report')
    yn_productdata = get_locater('EnIndex', 'yn_productdata')

    

