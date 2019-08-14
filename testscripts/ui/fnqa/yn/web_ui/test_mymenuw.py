# coding=utf-8

from testscripts.ui.fnqa.yn.web_ui.testbase import TestBase
from time import sleep
from testscripts.ui.fnqa.yn.page.po.web_ui.energy_web import MyMenuW, EnIndex

url_data_board = 'http://energy.test.tipaas.enncloud.cn/#/YesterdayEnergyBoard1'


# 测试用例: yn_web UI测试脚本demo


class MyMenuWTest(TestBase):
    def test_mymenuw_yesterday_energy_board(self):
        self.fn_web.click(EnIndex.yn_safe)
        sleep(1)
        try:
            self.fn_web.get_display(MyMenuW.yesterday_energy_board)
            print('用能分析已经展开')
            self.fn_web.click(MyMenuW.yesterday_energy_board)
            sleep(1)
            url = self.fn_web.get_url()
            self.assertEqual(url, url_data_board)
        except Exception as e:
            print("Exception found", format(e))
            print('用能分析没有展开')
            self.fn_web.click(MyMenuW.yn_analyze)
            sleep(1)
            self.fn_web.click(MyMenuW.yesterday_energy_board)
            sleep(1)
            url = self.fn_web.get_url()
            self.assertEqual(url, url_data_board)
