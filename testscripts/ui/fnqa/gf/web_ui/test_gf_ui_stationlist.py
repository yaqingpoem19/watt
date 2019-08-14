# coding=utf-8

from testscripts.ui.fnqa.gf.web_ui.testbase import TestBase
from time import sleep
from testscripts.ui.fnqa.gf.page.po.web_ui.pvs_web import InverterListPage, StationListPage, EvaluationPage, DispersionRatioAnalysisPage

general_url_board = 'http://pvs.test.tipaas.enncloud.cn/#/gf/general'


# 测试用例: 光伏web--光伏站列表页
class DemoTest(TestBase):
    def test_enter_data_board(self):

        self.fn_web.click(StationListPage.fushistation_button)
        sleep(1)
        url = self.fn_web.get_url()
        self.assertEqual(url, general_url_board)

    # def test_get_station_type(self):
    #     self.fn_web.open(statationlist_url_board)
    #     self.fn_web.F5()
    #     self.fn_web.click(DataBoard.self_station_type_arrow)
    #     sleep(2)
    #     station_types = self.fn_web.get_elements(DataBoard.self_station_type)
    #     list_station_types = list()
    #     for station_type in station_types:
    #         list_station_types.append(station_type.text)
    #     self.assertEqual(list_station_types[0], '泛能站')
    #     self.assertEqual(list_station_types[1], '光伏站')
    #
    # def test_pop_up_self_board(self):
    #     self.fn_web.open(url_data_board)
    #     self.fn_web.F5()
    #     self.fn_web.click(DataBoard.tab_self_data)
    #     sleep(2)
    #     self.fn_web.click(DataBoard.add_self_board)
    #     title = self.fn_web.get_element(AddSelfBoard.dialog_title).text
    #     sleep(2)
    #     self.assertEqual(title, '新增自定义看板')
