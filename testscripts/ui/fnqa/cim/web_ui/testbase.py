# coding=utf-8
import unittest
from pyui.pyweb import FanNengWeb
from utils.read_config import ReadCfgFile
from testscripts.ui.fnqa.cim.page.po.web_ui.maintain_web import LoginPage
from time import sleep


cfg = ReadCfgFile('demo_cfg.ini', 'web_ui')
test_login_url = cfg.get_val('ui_web', 'test_env_login')
browser = cfg.get_val('ui_web', 'browser')
user = cfg.get_val('ui_web', 'user')
pass_wd = cfg.get_val('ui_web', 'passwd')
# operation_index = cfg.get_val('ui_web', 'operation_index')


class TestBase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # 登录
        print("···········登录············")
        print("···········browser············", browser)
        print("···········url············", test_login_url)
        print()
        self.fn_web = FanNengWeb(browser)
        self.fn_web.max_window()
        self.fn_web.open(test_login_url)
        self.fn_web.type(LoginPage.user_name, user)
        self.fn_web.type(LoginPage.passwd, pass_wd)
        self.fn_web.click(LoginPage.submit_button)
        sleep(2)

    @classmethod
    def tearDownClass(self):
        print("···········退出浏览器············")
        # 关闭窗口并退出driver
        self.fn_web.close()
        self.fn_web.quit()


