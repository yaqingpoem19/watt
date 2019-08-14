# coding=utf-8
from testscripts.ui.fnqa.demo.web_ui.testbase import cfg
from testscripts.ui.fnqa.yn.web_ui.testbase import TestBase
from time import sleep
from testscripts.ui.fnqa.yn.page.po.web_ui.energy_web import EnIndex

operation_index = cfg.get_val('ui_web', 'operation_index')
url_yn_analyze = 'http://energy.test.tipaas.enncloud.cn/#/YesterdayEnergyBoard1'
url_yn_optimization = 'http://energy.test.tipaas.enncloud.cn/#/ElectricCostOptimization4'
url_yn_safe = 'http://energy.test.tipaas.enncloud.cn/#/TestingPowerkey3'
url_yn_report = 'http://energy.test.tipaas.enncloud.cn/#/TestingPowerkey3'
url_yn_productdata = 'http://energy.test.tipaas.enncloud.cn/#/TestingPowerkey3'


# 测试用例: yn_web UI测试脚本demo
class EnIndexTest(TestBase):
    def test_enindex_yn_analyze_url(self):
        self.fn_web.click(EnIndex.yn_analyze)
        sleep(1)
        url = self.fn_web.get_url()
        self.assertEqual(url, url_yn_analyze)

    def test_enindex_yn_optimization_url(self):
        self.fn_web.open(operation_index)
        self.fn_web.click(EnIndex.yn_optimization)
        sleep(1)
        url = self.fn_web.get_url()
        self.assertEqual(url, url_yn_optimization)

    def test_enindex_yn_safe_url(self):
        self.fn_web.open(operation_index)
        self.fn_web.click(EnIndex.yn_safe)
        sleep(1)
        url = self.fn_web.get_url()
        self.assertEqual(url, url_yn_safe)

    def test_enindex_yn_report_url(self):
        self.fn_web.open(operation_index)
        self.fn_web.click(EnIndex.yn_report)
        sleep(1)
        url = self.fn_web.get_url()
        self.assertEqual(url, url_yn_safe)

    def test_enindex_yn_productdata_url(self):
        self.fn_web.open(operation_index)
        self.fn_web.click(EnIndex.yn_productdata)
        sleep(1)
        url = self.fn_web.get_url()
        self.assertEqual(url, url_yn_safe)