# coding=utf-8

from testscripts.ui.fnqa.ai.testbase import TestBase
from utils.read_config import ReadCfgFile
from time import sleep
cfg = ReadCfgFile('ai_test_demo.ini', 'web_ui')
dc_zhan = cfg.get_val('ui_web', 'dc_zhan')
dc_zhan1 = cfg.get_val('ui_web', 'dc_zhan1')
dc_look2 = cfg.get_val('ui_web', 'dc_look2')
ys = cfg.get_val('ui_web', 'ys')
dc_download = cfg.get_val('ui_web', 'dc_download')
dc_return = cfg.get_val('ui_web', 'dc_return')
dc_x = cfg.get_val('ui_web', 'dc_x')
dc_y = cfg.get_val('ui_web', 'dc_y')
dc_ok = cfg.get_val('ui_web', 'dc_ok')
dc_editok = cfg.get_val('ui_web', 'dc_editok')


# AI能效曲线webu ui test demo
class coverTest(TestBase):

    def test_ai_cover(self):
        # 点击站信息下拉框
        self.fn_web.click(dc_zhan)
        ys1 = self.fn_web.get_element(ys).text
        self.assertEqual(ys1, '阶段能效曲线维护中心')
        sleep(1)
        # 选择龙游站
        self.fn_web.click(dc_zhan1)
        ly = self.fn_web.get_element(dc_zhan1).text
        self.assertEqual(ly, '龙游站')
        sleep(1)
        # 点击下载按钮
        self.fn_web.click(dc_download)
        sleep(1)
        # 点击第二个查看按钮
        self.fn_web.click(dc_look2)
        sleep(1)
        # 清除第一个X值
        self.fn_web.clear(dc_x)
        sleep(1)
        # 第一个X值输入100
        self.fn_web.type(dc_x, 100)
        sleep(1)
        # 点击保存
        self.fn_web.click(dc_editok)
        sleep(1)
        # 点击确认
        self.fn_web.click(dc_ok)
        sleep(1)
        # 点击返回
        self.fn_web.click(dc_return)
        sleep(5)