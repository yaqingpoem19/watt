# coding=utf-8
import pymysql
import unittest
import datetime
import redis
import time
import re

from pyrest.yw_api import FanNengAPI
from utils.read_config import ReadCfgFile
from utils.jsonparse import parser

endpoint_ywWeb_login = ReadCfgFile('yw_cfg.ini').get_val('rest_api', 'endpoint_ywWeb_login')
endpoint_yw_cim = ReadCfgFile('yw_cfg.ini').get_val('rest_api', 'endpoint_yw_cim')
endpoint_yw_web = ReadCfgFile('yw_cfg.ini').get_val('rest_api', 'endpoint_yw_web')
username_web = ReadCfgFile('yw_cfg.ini').get_val('rest_api', 'username1')
pwd_web = ReadCfgFile('yw_cfg.ini').get_val('rest_api', 'web_passwd')
mark = ReadCfgFile('yw_cfg.ini').get_val('rest_api', 'mark')
vcode = ReadCfgFile('yw_cfg.ini').get_val('rest_api', 'vcode')
# login_data_web = {"mark": mark, "pwd": pwd_web, "username": username_web, "vcode": vcode}
# login_data_web = {"username": "testad111", "pwd": "123456", "vcode": "1234", "mark": "rCnVc9Or"}
access = {"appid": "1", "appsecret": "123456"}


# 测试环境
base_ip = '10.39.30.21'
base_name = 'wit-operation'
base_pwd = 'wit-operation'
base_ku = 'wit-operation'

# 测试环境
user_ip = '10.39.30.21'
user_name = 'platform'
user_pwd = '1qazXSW@3edc'
user_ku = 'fnw-boss'

# 测试
link_ip = '10.39.30.21'
link_name = 'fn_db_test'
link_pwd = 'fn_db_test20180411'
link_ku = 'fannengdb'


class YWWebLogin(unittest.TestCase):
    # 登陆
    def setUp(self):
        self.login = FanNengAPI(endpoint_ywWeb_login)
        # self.login.mark(mark)
        # self.assertEqual(self.login.rest.response.status_code, 200)
        # check_vode = {"vcode": vcode, "mark": mark}
        # self.login.check_vcode(check_vode)
        # self.assertEqual(self.login.rest.response.status_code, 200)
        login_data_web = "username="+username_web+"&password=123abc"
        # login_data_web = {}
        self.login.login(login_data_web)
        self.assertEqual(self.login.rest.response.status_code, 200)
        json = self.login.rest.json_result()
        self.token = parser(json, '$.data')[0].get('ticket')
        self.headers = {'token': self.token}
        self.openid = parser(json, '$.data')[0].get('userEnt').get('openid')

    # def access_token(self):
    #     self.login = FanNengAPI(endpoint_ywWeb_login)
    #     self.login.get_token(access)
    #     json = self.login.rest.json_result()
    #     self.assertEqual(self.login.rest.response.status_code, 200)
    #     access_token = parser(json, '$.data')[0].get('access_token')
    #     return access_token

    # 基础数据库
    def db_base(self, sql):
        self.ip = base_ip
        self.name = base_name
        self.password = base_pwd
        self.ku = base_ku
        self.sql = sql
        db = pymysql.connect(base_ip, base_name, base_pwd, base_ku, charset='utf8')
        cursor = db.cursor()
        u = cursor.fetchmany(cursor.execute(sql))
        return u

    # 用户数据库
    def db_user(self, sql):
        self.ip = user_ip
        self.name = user_name
        self.password = user_pwd
        self.ku = user_ku
        self.sql = sql
        db = pymysql.connect(user_ip, user_name, user_pwd, user_ku, charset='utf8')
        cursor = db.cursor()
        u = cursor.fetchmany(cursor.execute(sql))
        return u

    # 衔接数据库
    def db_link(self, sql):
        self.ip = link_ip
        self.name = link_name
        self.password = link_pwd
        self.ku = link_ku
        self.sql = sql
        db = pymysql.connect(link_ip, link_name, link_pwd, link_ku, charset='utf8')
        cursor = db.cursor()
        u = cursor.fetchmany(cursor.execute(sql))
        return u

    # 添加数据库操作
    def db_insert(self, sql):
        self.ip = base_ip
        self.name = base_name
        self.password = base_pwd
        self.ku = base_ku
        self.sql = sql
        db = pymysql.connect(base_ip, base_name, base_pwd, base_ku, charset='utf8')
        cursor = db.cursor()
        cursor.execute(sql)
        rowcount = cursor.rowcount
        db.commit()
        cursor.close()
        db.close()
        return rowcount

    # 添加数据库操作
    def db_link_insert(self, sql):
        self.ip = link_ip
        self.name = link_name
        self.password = link_pwd
        self.ku = link_ku
        self.sql = sql
        db = pymysql.connect(link_ip, link_name, link_pwd, link_ku, charset='utf8')
        cursor = db.cursor()
        cursor.execute(sql)
        rowcount = cursor.rowcount
        db.commit()
        cursor.close()
        db.close()
        return rowcount

    def db_base_update(self, sql):
        self.ip = base_ip
        self.name = base_name
        self.password = base_pwd
        self.ku = base_ku
        self.sql = sql
        db = pymysql.connect(base_ip, base_name, base_pwd, base_ku, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        db.close()

    # 自定义指标处理时间
    @staticmethod
    def panel_time(num):
        star = "2018-07-16 17:06:30"
        end = "2018-07-17 17:06:30"
        if num == 1:  # 1min   1分钟
            time1 = "2018-07-16 17:07:00"
        elif num == 5:  # 5分钟
            time1 = "2018-07-16 17:10:00"
        elif num == 15:  # 15分钟
            time1 = "2018-07-16 17:15:00"
        elif num == 60:  # 60分钟
            time1 = "2018-07-16 18:00:00"
        elif num == 1440:  # 1天
            time1 = "2018-07-17 00:00:00"
        time_list = []
        time_start = datetime.datetime.strptime(time1, '%Y-%m-%d %H:%M:%S')
        time_end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        time_list.append(time1)
        while (time_start + datetime.timedelta(minutes=num)) < time_end:
            time_start += datetime.timedelta(minutes=num)
            time_list.append(time_start.strftime('%Y-%m-%d %H:%M:%S'))
        return time_list

    # 站信息-所有
    def cim_station_all(self):
        self.fn_cim = FanNengAPI(endpoint_yw_cim)
        # self.fn_cim.rest.session.headers.update(self.headers)
        payload = {
            "pageNumber": 0,
            "pageSize": 10000,
            "status": "OPR"
        }
        self.fn_cim.post_cim_station_all(payload)
        json = self.fn_cim.rest.json_result()
        containerList = parser(json, '$.containerList')[0]
        station_list = []
        for data in containerList:
            station = {"id": "CA02ES01", "name": "龙游城南工业园", "cimId": 2}
            station.update(id=data.get("containerId"))
            station.update(name=data.get("containerName"))
            station.update(cimId=data.get("cimId"))
            station_list.append(station)
        # print(station_list)
        return station_list

    # 站信息-业务域
    def cim_station(self, parameter):
        self.fn_cim = FanNengAPI(endpoint_yw_cim)
        self.fn_cim.rest.session.headers.update(self.headers)
        payload = {
            "containerType": [
                parameter
            ]
        }
        self.fn_cim.post_get_cim_station(payload)
        json = self.fn_cim.rest.json_result()
        station_list = []
        for data in json:
            station = {"cimId": 2, "containerId": "CA02ES01", "containerName": "龙游城南工业园"}
            station.update(cimId=data.get("cimId"))
            station.update(containerId=data.get("containerId"))
            station.update(containerName=data.get("containerName"))
            station_list.append(station)
        return station_list

    # 设备类型
    def equipment_type(self, parameter):
        self.fn_cim = FanNengAPI(endpoint_yw_cim)
        self.fn_cim.rest.session.headers.update(self.headers)
        payload = {
            "containerCimId": parameter
        }
        self.fn_cim.post_get_cim_equip_type(payload)
        json = self.fn_cim.rest.json_result()
        equipment_type_list = []
        for data in json:
            equip_type = {"id": 2, "name": "燃气蒸汽锅炉", "alias": "GSB"}
            equip_type.update(id=data.get("id"))
            equip_type.update(name=data.get("name"))
            equip_type.update(alias=data.get("alias"))
            equipment_type_list.append(equip_type)
        return equipment_type_list

    # 设备编号
    def equipment_code(self, cim_id, device_type):
        self.fn_cim = FanNengAPI(endpoint_yw_cim)
        self.fn_cim.rest.session.headers.update(self.headers)
        payload = {
            "containerCimId": cim_id,
            "deviceType": device_type,
            "pageNumber": 1,
            "pageSize": 100000
        }
        self.fn_cim.post_get_cim_device(payload)
        json = self.fn_cim.rest.json_result()
        device_list = parser(json, '$.deviceList')[0]
        equipment_code_list = []
        for data in device_list:
            equip_code = {"cimId": 2, "deviceId": "HRSG_HRSG01", "description": "蒸汽型余热锅炉"}
            equip_code.update(cimId=data.get("cimId"))
            equip_code.update(deviceId=data.get("deviceId"))
            value = data.get("description")  # + '_' + data.get("deviceName")
            equip_code.update(description=value)
            equipment_code_list.append(equip_code)
        return equipment_code_list

    # 设备指标
    def metric_code(self, cim_id):
        self.fn_cim = FanNengAPI(endpoint_yw_cim)
        self.fn_cim.rest.session.headers.update(self.headers)
        payload = {
            "deviceCimId": cim_id,
            "pageNumber": 0,
            "pageSize": 100000
        }
        self.fn_cim.post_get_cim_metric(payload)
        json = self.fn_cim.rest.json_result()
        metric_list = parser(json, '$.metricList')[0]
        metric_code_list = []
        for data in metric_list:
            metric_code = {"cimId": 2, "metricId": "GSB_GSB01_FwInt", "name": "FwInt", "description": "1#燃气锅炉给水管累计流量"}
            metric_code.update(cimId=data.get("cimId"))
            metric_code.update(metricId=data.get("metricId"))
            metric_code.update(name=data.get("name"))
            metric_code.update(description=data.get("description"))
            metric_code_list.append(metric_code)
        return metric_code_list

    # 设备指标
    def metric_code_all(self, cim_id):
        self.fn_cim = FanNengAPI(endpoint_yw_cim)
        self.fn_cim.rest.session.headers.update(self.headers)
        payload = {
            "deviceCimId": cim_id,
            "pageNumber": 0,
            "pageSize": 100000
        }
        self.fn_cim.post_get_cim_metric(payload)
        json = self.fn_cim.rest.json_result()
        metric_list = parser(json, '$.metricList')[0]
        return metric_list

    # 获取站点的所有指标
    def station_metric_code(self, station_name):
        self.fn_cim = FanNengAPI(endpoint_yw_cim)
        self.fn_cim.rest.session.headers.update(self.headers)
        payload = {
            "containerId": station_name
        }
        self.fn_cim.post_station_metric_all(payload)
        json = self.fn_cim.rest.json_result()
        metric_list = []
        for value in json:
            metric = {}
            metric.update(cimId=value.get('cimId'))
            metric.update(equiCimId=value.get('equiCimId'))
            metric.update(metricId=value.get('metricId'))
            metric.update(description=value.get('description'))
            metric_list.append(metric)
        return metric_list

    # 获取用户信息
    def user_info(self, token):
        # token = "a89fbf174de94d5d857b3456d8ac3e95"
        self.login = FanNengAPI(endpoint_ywWeb_login)
        self.login.get_user_info(token)

        json = self.login.rest.json_result()

        return json

    # 连接redis-根据key获取value
    def collection_redis(self, redis_id):
        # redis_id = "5E9BF7DE5E4946769F31206F769F9CE0"
        ticket = self.token
        # access_token = self.access_token()
        data = self.user_info(ticket)
        user_login_name = data.get('openid')
        r = redis.Redis(host='10.39.30.2', port=6379, password='FNadmin1234', db=9, encoding='utf-8')
        key_id_list = self.get_redis_kye()
        if redis_id not in key_id_list:
            redis_data = None
        else:
            key_id = "DATA_ANALYSIS_ACTION:" + user_login_name + ":" + redis_id
            redis_data = r.get(key_id).decode()
            global null
            null = None
            redis_data = eval(redis_data)
            redis_data = redis_data[1]
            start_time = redis_data.get('startTime')[1]
            start_time /= 1000.0
            start_time = time.localtime(start_time)
            s_t = time.strftime("%Y-%m-%d %H:%M:%S", start_time)
            redis_data.update(startTime=s_t)
            end_time = redis_data.get('endTime')[1]
            end_time /= 1000.0
            end_time = time.localtime(end_time)
            e_t = time.strftime("%Y-%m-%d %H:%M:%S", end_time)
            redis_data.update(endTime=e_t)
            redis_vo = redis_data.get('paramRedisVos')[1]
            redis_vo_list = []
            for va in redis_vo:
                redis_vo_list.append(va[1])
            redis_data.update(paramRedisVos=redis_vo_list)
        return redis_data

    # 获取所有的value
    def get_redis_value_all(self):
        ticket = self.token
        # access_token = self.access_token()
        data = self.user_info(ticket)
        user_login_name = data.get('openid')
        r = redis.Redis(host='10.39.30.2', port=6379, password='FNadmin1234', db=9, encoding='utf-8')
        key_id_list = self.get_redis_kye()
        value_data = []
        for redis_id in key_id_list:
            key_id = "DATA_ANALYSIS_ACTION:" + user_login_name + ":" + redis_id
            redis_data = r.get(key_id).decode()
            global null
            null = None
            redis_data = eval(redis_data)
            redis_data = redis_data[1]
            start_time = redis_data.get('startTime')[1]
            start_time /= 1000.0
            start_time = time.localtime(start_time)
            s_t = time.strftime("%Y-%m-%d %H:%M:%S", start_time)
            redis_data.update(startTime=s_t)
            end_time = redis_data.get('endTime')[1]
            end_time /= 1000.0
            end_time = time.localtime(end_time)
            e_t = time.strftime("%Y-%m-%d %H:%M:%S", end_time)
            redis_data.update(endTime=e_t)
            redis_vo = redis_data.get('paramRedisVos')[1]
            redis_vo_list = []
            for va in redis_vo:
                redis_vo_list.append(va[1])
            redis_data.update(paramRedisVos=redis_vo_list)
            value_data.append(redis_data)
        return value_data

    # 获取所有的key
    def get_redis_kye(self):
        ticket = self.token
        # access_token = self.access_token()
        data = self.user_info(ticket)
        user_login_name = data.get('openid')
        r = redis.Redis(host='10.39.30.2', port=6379, password='FNadmin1234', db=9, encoding='utf-8')
        key = "DATA_ANALYSIS_ACTION:" + user_login_name + "*"
        keys = r.keys(pattern=key)
        redis_id_list = []
        for va in keys:
            key_value = str(va)
            str1 = "b'DATA_ANALYSIS_ACTION:" + user_login_name + ":"
            redis_id = re.findall(str1 + "(.*)'", key_value)
            redis_id_list.append(redis_id[0])
        return redis_id_list
