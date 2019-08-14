# coding=utf-8

from testscripts.ui.fnqa.demo.web_ui.testbase import TestBase
from time import sleep
from testscripts.ui.fnqa.demo.page.po.web_ui.maintain_web import NavBar, DataBoard, AddSelfBoard

url_data_board = 'http://fe-test-maintain-628-fnw-test.tipaas.enncloud.cn/#/yw/data'


# 测试用例: 运维web UI测试脚本demo
class DemoTest(TestBase):
    def test_enter_data_board(self):

        self.fn_web.click(NavBar.tool_arrow)
        sleep(1)
        self.fn_web.click(NavBar.data_board)
        sleep(1)
        url = self.fn_web.get_url()
        self.assertEqual(url, url_data_board)

    def test_get_station_type(self):
        self.fn_web.open(url_data_board)
        self.fn_web.F5()
        self.fn_web.click(DataBoard.self_station_type_arrow)
        sleep(2)
        station_types = self.fn_web.get_elements(DataBoard.self_station_type)
        list_station_types = list()
        for station_type in station_types:
            list_station_types.append(station_type.text)
        self.assertEqual(list_station_types[0], '泛能站')
        self.assertEqual(list_station_types[1], '光伏站')

    def test_pop_up_self_board(self):
        self.fn_web.open(url_data_board)
        self.fn_web.F5()
        self.fn_web.click(DataBoard.tab_self_data)
        sleep(2)
        self.fn_web.click(DataBoard.add_self_board)
        title = self.fn_web.get_element(AddSelfBoard.dialog_title).text
        sleep(2)
        self.assertEqual(title, '新增自定义看板')
