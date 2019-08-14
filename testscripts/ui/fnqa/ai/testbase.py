# coding=utf-8
import unittest
from pyui.pyweb import FanNengWeb
from utils.read_config import ReadCfgFile
from time import sleep


cfg = ReadCfgFile('ai_test_demo.ini', 'web_ui')
test_login_url = cfg.get_val('ui_web', 'test_env_login')
browser = cfg.get_val('ui_web', 'browser')
dc_password = cfg.get_val('ui_web', 'dc_password')
passwd = cfg.get_val('ui_web', 'passwd')
dc_login = cfg.get_val('ui_web', 'dc_login')


class TestBase(unittest.TestCase):
    fn_web = FanNengWeb(browser)

    @classmethod
    def setUpClass(self):
        self.fn_web.open(test_login_url)
        self.fn_web.type(dc_password, passwd)
        self.fn_web.click(dc_login)
        sleep(2)
        # self.fn_web.open(operation_index)

    @classmethod
    def tearDownClass(self):
        # 关闭窗口并退出driver
        self.fn_web.close()
        self.fn_web.quit()


