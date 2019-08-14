# coding=utf-8

from testscripts.ui.fnqa.cim.web_ui.testbase import TestBase
from time import sleep
from testscripts.ui.fnqa.cim.page.po.web_ui.maintain_web import NavBar,DevicePage

url_data_board = 'http://cim-platform-fnw-release.topaas.enncloud.cn/admin/index.html'


# 测试用例: cim UI测试脚本demo
class DemoTest(TestBase):
    def test_enter_device_board(self):
        print("test_enter_device_board function·········进入设备实例页面······")
        self.fn_web.click(NavBar.cim_act)
        self.fn_web.click(NavBar.act_device)
        sleep(3)
        self.fn_web.switch_to_frame(DevicePage.iframe_device)
        button_text = self.fn_web.get_element(DevicePage.add_device).text
        self.assertEqual("添加设备", button_text)

        self.fn_web.select_input(DevicePage.park_selector, DevicePage.select_park05)
        # self.fn_web.click(DevicePage.park_selector)
        # self.fn_web.click(DevicePage.select_park05)
        self.fn_web.click(DevicePage.seach_system)
        sleep(1)
        print("··········重新选择园区查询成功········")
        self.fn_web.get_windows_img('foo.png')
        print("··········截屏成功········")

        device_code01_text = self.fn_web.get_element(DevicePage.device_code01).text
        self.assertEqual("WMFOD_WMFOD01", device_code01_text, msg="第一个设备的设备编码与预期不一致")

        # self.fn_web.click(DevicePage.add_device)
        # print("····添加设备页面已打开·····")
        # sleep(1)
        # self.fn_web.type(DevicePage.add_device_name, "123")
        # print("输入设备名称")

        '''
        # station_types = self.fn_web.get_elements(DataBoard.self_station_type)
        # list_station_types = list()
        # for station_type in station_types:
        #     list_station_types.append(station_type.text)
        # self.assertEqual(list_station_types[0], '泛能站')
        # self.assertEqual(list_station_types[1], '光伏站')
        # 
        # title = self.fn_web.get_element(AddSelfBoard.dialog_title).text
        # self.assertEqual(title, '新增自定义看板')
        '''


