# coding=utf-8
from utils.read_config import ReadCfgFile
from utils.jsonparse import parser
from pyrest.ai_api import AiAPI
from testscripts.api.fnqa.ai.simpletestbase import aibase
import json
url = ReadCfgFile('ai_cfg.ini').get_val('rest_ai_api', 'fhyc_test')
url1 = ReadCfgFile('ai_cfg.ini').get_val('rest_ai_api', 'yxcl_test')
url2 = ReadCfgFile('ai_cfg.ini').get_val('rest_ai_api', 'fhpy_test')


class TestBaseAI(aibase):
    # 负荷预测，返回预测列表
    def ailoadForecasting(self, time, queries, loadType=4):
      	# loadType = 预测类型（1 heatWater，2elec，3cool，4steam，默认值4）
        # time = 时间戳，预测time时间后(结果不含time)的12个小时的值，只接收整点
        # staId = 站ID，字符串类型
        # equipID = 设备，字符串类型
        # metric = 采集点，字符串类型
        # equipMK = 设备标识
        list1 = []
        sumtim = 503
        # metric1 = "UES."+metric
        # queries = [{"aggregator": "none", "downsample": "1h-first-zero", "metric": metric1, "tags":
        #    {"equipID": equipID, "staId": staId, "equipMK": equipMK}}]
        # 获取time时间前504小时数据
        json1 = self.opstpdatereduce(time, sumtim, queries)
        payload = {
            "inputData": {
                'CEU_FIQ303_FsIntLP': json1},
            "containerID": "containerID",
          	"loadType": loadType,
            "targetDeviceID": "targetDeviceID",
            "nextNum": "24",
            "modelType": "loadPredict",
            "bakParamMap": {}}

        self.load = AiAPI(url)
        self.load.load_forecasting(payload)
        try:
            self.assertEqual(self.load.rest.response.status_code, 200)
            json3 = self.load.rest.json_result()
            msg1 = parser(json3, '$.data.loads')[0]
            targetDeviceID = msg1[1]['targetDeviceID']
            self.assertEqual(targetDeviceID, 'targetDeviceID')
        except:
            print("AI接口错误")
            raise TypeError
        for i in msg1:
            zd = {"time":i['time'],"value":i['value']}
            list1.append(zd)
        return list1

    def RunStrategy(self, time, queries):
        # 调度优化，queries入参是整站设备(不含CCHP)
        # time = 时间戳，调度优化time后4小时(结果含time)，只接收整点
        # queries = 站下所有需要调度得设备
        # 例[{"aggregator": "none", "metric": "UES.FsInt", "tags":{"equipID": "GSB01", "staId":staId, "equipMK": "GSB"}}]
        # 只修改equipID，staId，equipMK即可使用
        # metric = 测点
        # equipID = 设备
        # staId = 站ID
        # equipMK = 设备标识
        # 输出结果为每台设备4小时的调度状态，flag = 1是开启0是关闭，rate = 负荷率，gE = 燃气消耗量，hESt = 产蒸汽量
        # max_profit = 最大利润，resultStatus = 是否最尤
        sumtim = 4
        ca=[]
        ca1 = []
        equipID = []
        # 拼接大数据入参
        for i in range(len(queries)):
            ca.append(list(ca1))  # 必须强转，勿动，勿动
            gsb = queries[i]['tags']['equipMK'] + '_' + queries[i]['tags']['equipID']
            equipID.append(gsb)
        # 查询所有采集点数据
        json1 = self.getz3(time, sumtim, queries,ca)
        # print(json.dumps(json1))
        # 计算设备的起停状态
        isOffMap = {}
        for x in range(len(queries)):
            if json1[x][0]['value'] > 0:
                GSB01isOff = "1"
            else:
                GSB01isOff = "0"
            isOffMap[equipID[x]] = GSB01isOff

        # print(json.dumps(json1))
        # 计算loads
        loads = []
        for xx in range(sumtim):
            values = 0.0
            for xxx in range(len(queries)):
                values += json1[xxx][xx]['value']
            loadszd = {"containerID": "Anxing", "value": str(values), "elecValue": "", "coolValue": "", "heatWaterValue": "", "targetDeviceID": "GongNengCe","time": str(time + xx * 3600)}
            loads.append(loadszd)
        # 拼入参
        payload = {
            "isOffMap": isOffMap,
            "loads": loads,
            "nextNum": str(sumtim),
            "modelType": "runPolicy",
            "containerID": "CA01ES01",
            "bakParamMap": {}
        }
        # print(json.dumps(payload))
        # print("请求参数：%s"% json.dumps(payload))
        self.load = AiAPI(url1)
        self.load.running_strategy(payload)
        try:
            self.assertEqual(self.load.rest.response.status_code, 200)
            json3 = self.load.rest.json_result()
            self.assertEqual(json3['data']['policyMap'][equipID[0]][0]['time'], str(time))
        except:
            print("运行调度接口报错'\n'请求参数：%s" % json.dumps(payload))
            raise TypeError
        # print("请求参数：%s" % json.dumps(json3))
        return json3

    def loadTranslation(self, time1):
        # 负荷平移
        # time1 = 时间戳，是结束平移的时间，返回结果是龙游的平移结果
        # offset 负数是向前移，正数是向后移
        # moveCost 移动之后的总成本
        staId = "CA02ES01"
        time = time1
        sumtim = 24
        queries = [{"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "SFSX", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "DZWJ", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "TRHX", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "HDL", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "WMSC", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "XBZJ", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "LGSL", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "TNSP", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "CXLY", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "JDKJ", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "SSSX", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "LCCW", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "HGYSY", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "YMLY", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "TMZY", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "QLBZJ", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "DDMN", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "FDLHC", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "CDSX", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "LYXCL", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "MHSP", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "FTZZ", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "JDJJ", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "ZYH", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "HSGM", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "SJSJ", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "CYHG", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "NNHZY", "staId": staId, "equipMK": "CEU"}},
                   {"aggregator": "none", "metric": "UES.FsIntLP",
                    "tags": {"equipID": "LHDD", "staId": staId, "equipMK": "CEU"}}]
        ca = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
              [], [], []]
        ca1 = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
               [], [], []]
        self.entId1 = ["FIQ202_顺丰水洗蒸汽累计流量", "FIQ204_德州五金蒸汽累计流量", "FIQ205_天瑞化学蒸汽累计流量", "FIQ206_惠多利蒸汽累计流量",
                       "FIQ207_外贸笋厂蒸汽累计流量", "FIQ208_信邦助剂蒸汽累计流量", "FIQ209_利光塑料蒸汽累计流量", "FIQ210_铜鸟食品蒸汽累计流量",
                       "FIQ211_百依家纺蒸汽累计流量", "FIQ214_九鼎科技蒸汽累计流量", "FIQ215_苏盛水洗蒸汽累计流量", "FIQ216_鹿成宠物蒸汽累计流量",
                       "FIQ217_桦固优实业蒸汽累计流量", "FIQ218_元美铝业蒸汽累计流量", "FIQ219_特美纸业蒸汽累计流量", "FIQ220_群力标准件蒸汽累计流量",
                       "FIQ221_大地毛呢蒸汽累计流量", "FIQ222_福德利花材蒸汽累计流量", "FIQ240_辰东水洗蒸汽累计流量", "FIQ241_力源新材料蒸汽累计流量",
                       "FIQ244_美哈食品蒸汽累计流量", "FIQ251_福田造纸蒸汽累计流量", "FIQ252_家德家具蒸汽累计流量", "FIQ212_正一煌蒸汽流量累计流量",
                       "FIQ213_汉桑工贸蒸汽流量累计流量", "FIQ261_瞬杰塑胶蒸汽流量累计流量", "FIQ203_辰阳化工蒸汽流量累计流量",
                       "FIQ253_年年虹纸业蒸汽累计流量", "FIQ201_龙辉电镀蒸汽累计流量"]
        # 查询大数据接口
        aa = self.getz3(time, sumtim, queries, ca)
        vo = []
        for i in range(len(queries)):
            for ii in range(sumtim):
                vo.append(aa[i][ii]['value'])
            ca1[i].append(vo)
            vo = []
        # 拼请求AI平移接口参数
        self.entIdA = [[self.entId1[0], ca1[0][0], 1, 2, 24], [self.entId1[1], ca1[1][0], 1, 2, 24],
                       [self.entId1[2], ca1[2][0], 1, 2, 24],
                       [self.entId1[3], ca1[3][0], 1, 2, 24], [self.entId1[4], ca1[4][0], 1, 2, 24],
                       [self.entId1[5], ca1[5][0], 1, 2, 24],
                       [self.entId1[6], ca1[6][0], 1, 2, 24], [self.entId1[7], ca1[7][0], 1, 2, 24],
                       [self.entId1[8], ca1[8][0], 1, 2, 24],
                       [self.entId1[9], ca1[9][0], 1, 2, 24], [self.entId1[10], ca1[10][0], 1, 2, 24],
                       [self.entId1[11], ca1[11][0], 1, 2, 24],
                       [self.entId1[12], ca1[12][0], 1, 2, 24], [self.entId1[13], ca1[13][0], 1, 2, 24],
                       [self.entId1[14], ca1[14][0], 1, 2, 24],
                       [self.entId1[15], ca1[15][0], 1, 2, 24], [self.entId1[16], ca1[16][0], 1, 2, 24],
                       [self.entId1[17], ca1[17][0], 1, 2, 24],
                       [self.entId1[18], ca1[18][0], 1, 2, 24], [self.entId1[19], ca1[19][0], 1, 2, 24],
                       [self.entId1[20], ca1[20][0], 1, 2, 24],
                       [self.entId1[21], ca1[21][0], 1, 2, 24], [self.entId1[22], ca1[22][0], 1, 2, 24],
                       [self.entId1[23], ca1[23][0], 1, 2, 24],
                       [self.entId1[24], ca1[24][0], 1, 2, 24], [self.entId1[25], ca1[25][0], 1, 2, 24],
                       [self.entId1[26], ca1[26][0], 1, 2, 24],
                       [self.entId1[27], ca1[27][0], 1, 2, 24], [self.entId1[28], ca1[28][0], 1, 2, 24]]
        section = [{"from": "0", "to": "5", "cost": "312.09236845454546"},
                   {"from": "5", "to": "10", "cost": "261.94823166393445"},
                   {"from": "10", "to": "15", "cost": "235.61446645312498"},
                   {"from": "15", "to": "25", "cost": "240.16313305555556"},
                   {"from": "25", "to": "35", "cost": "225.15273123529408"}]
        payload = self.translationDate(self.entIdA, section)
        # print(payload)
        total = self.translationCost(self.entIdA, section)
        self.load = AiAPI(url2)
        self.load.load_translation(payload)
        self.assertEqual(self.load.rest.response.status_code, 200)
        json1 = self.load.rest.json_result()
        # print(json.dumps(json1))
        try:
            moveCost = float(parser(json1, '$.data.moveCost')[0])
        except:
            print("负荷平移接口返回错误'\n'请求参数：%s'\n'接口返回：%s" % (payload, json1))
            raise TypeError
        returnEntId = parser(json1, '$.data.moveData')[0]
        returnEntId1 = []
        returnEntId2 = []
        for i in range(len(self.entIdA)):
            returnEntId1.append(str(self.entIdA[i][0]))
            returnEntId2.append(str(returnEntId[i]['entId']))
        # 对比2个列表,验证返回的entId
        self.assertListEqual(returnEntId1, returnEntId2)
        # 计算平移后成本
        tota2 = self.translationAfterCost(self.entIdA, json1, section)
        if moveCost != tota2:
            raise TypeError
        else:
            return json1