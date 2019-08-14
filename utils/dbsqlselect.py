# coding=utf-8
import pymysql
import unittest

from pyrest.yw_api import FanNengAPI
from utils.read_config import ReadCfgFile
from utils.jsonparse import parser

endpoint_yw_app = ReadCfgFile('yw_cfg.ini').get_val('rest_api', 'endpoint_yw_app')
username = ReadCfgFile('yw_cfg.ini').get_val('rest_api', 'username4')
pwd = ReadCfgFile('yw_cfg.ini').get_val('rest_api', 'passwd')
imei = ReadCfgFile('yw_cfg.ini').get_val('rest_api', 'imei')
login_data = {"loginName": username, "pwd": pwd, "imei": imei, "phoneType": "ios"}


# 预生产地址-苏晔
# base_ip = '10.39.48.241'
# base_name = 'wit-operation'
# base_pwd = 'wit-operation'
# base_ku = 'wit-operation'

# 开发环境
# base_ip = '10.39.30.22'
# base_name = 'wit-operation'
# base_pwd = 'wit-operation'
# base_ku = 'wit-operation'

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


# 各种数据库的封装
class DBRequest(unittest.TestCase):
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
            u = cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        db.close()
        return u

    def db_link_update(self, sql):
        self.ip = link_ip
        self.name = link_name
        self.password = link_pwd
        self.ku = link_ku
        self.sql = sql
        db = pymysql.connect(link_ip, link_name, link_pwd, link_ku, charset='utf8')
        cursor = db.cursor()
        try:
            u = cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
        db.close()
        return u

    def tearDown(self):
        payload = {"token": self.token}
        self.logout = FanNengAPI(endpoint_yw_app)
        self.logout.rest.session.headers.update(self.headers)
        self.logout.yw_app_logout(payload)
        self.assertEqual(self.logout.rest.response.status_code, 200)
        json = self.logout.rest.json_result()
        code = parser(json, '$.code')[0]
        self.assertEqual(code, 0)

    def setUp(self):
        self.login = FanNengAPI(endpoint_yw_app)
        self.login.yw_app_login(login_data)
        self.assertEqual(self.login.rest.response.status_code, 200)
        json = self.login.rest.json_result()
        self.openid = parser(json, '$.openId')[0]
        self.token = parser(json, '$.token')[0]
        self.headers = {'token': self.token}



