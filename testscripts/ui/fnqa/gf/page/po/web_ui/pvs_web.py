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


class InverterListPage:
    firstinverterdetail_botton = get_locater('InverterListPage', 'firstinverterdetail_botton')
    backtostationlist_botton = get_locater('InverterListPage', 'backtostationlist_botton')

    
class StationListPage:
    fushistation_button = get_locater('StationListPage', 'fushistation_button')
    kanghuistation_button = get_locater('StationListPage', 'kanghuistation_button')

    
class EvaluationPage:
    aidiagnose_botton = get_locater('EvaluationPage', 'aidiagnose_botton')
    dispersion_botton = get_locater('EvaluationPage', 'dispersion_botton')
    energyefficiency_botton = get_locater('EvaluationPage', 'energyefficiency_botton')
    monitor_botton = get_locater('EvaluationPage', 'monitor_botton')

    
class LoginPage:
    submit_button = get_locater('LoginPage', 'submit_button')
    passwd = get_locater('LoginPage', 'passwd')
    check_vode = get_locater('LoginPage', 'check_vode')
    user_name = get_locater('LoginPage', 'user_name')

    
class DispersionRatioAnalysisPage:
    combo_box = get_locater('DispersionRatioAnalysisPage', 'combo_box')

    

