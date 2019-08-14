# __*__coding=utf-8__*__
# autor 张鹏
# date  2018/5/23
# describe 数据库操作函数

from utils.read_config import ReadCfgFile
#import  utils.dbsqlselect.DBRequest as DBRequest
import pymysql
#import pyMySQLdb
class dbUtil() :

    def __init__(self):
        # 获取基础数据连接信息
        self.base_ip= ReadCfgFile().get_val('database', 'base_ip')
        self.base_name=ReadCfgFile().get_val('database', 'base_name')
        self.base_pwd=ReadCfgFile().get_val('database', 'base_pwd')
        self.base_ku=ReadCfgFile().get_val('database', 'base_ku')
        #获取用户库连接信息
        # self.user_ip= ReadCfgFile().get_val('database', 'user_ip')
        # self.user_name=ReadCfgFile().get_val('database', 'user_name')
        # self.user_pwd=ReadCfgFile().get_val('database', 'user_pwd')
        # self.user_ku=ReadCfgFile().get_val('database', 'user_ku')

    def baseDB_conn(self):
        print (self.base_ip, self.base_name, self.base_pwd, self.base_ku)
        try:
            base_conn = pymysql.connect(self.base_ip, self.base_name, self.base_pwd, self.base_ku,charset="gbk",cursorclass=pymysql.cursors.DictCursor)#返回字典类型

            return base_conn
        except:
            print ("连接base数据库时出错！")
    def userDB_conn(self):
        try:
            user_conn = pymysql.connect(self.user_ip, self.user_name, self.user_pwd, self.user_ku,charset="gbk",cursorclass=pymysql.cursors.DictCursor)#返回字典类型
            return user_conn
        except:
            print("连接base数据库时出错！")

    #base数据库查询一条数据，返回字典
    def selectOne_base(self,sql):
        cursor =self.baseDB_conn().cursor()
        cursor.execute(sql)
        result=cursor.fetchone()
        cursor.close()
        return result

    # base数据库查询多条数据，返回字典列表
    def selectMany_base(self,sql,size):
        cursor =self.baseDB_conn().cursor()
        cursor.execute(sql)
        result=cursor.fetchmany(size)
        cursor.close()

        return result

    # base数据库查询多条数据，返回字典列表
    def selectAll_base(self,sql):
        cursor =self.baseDB_conn().cursor()
        cursor.execute(sql)
        result=cursor.fetchall()
        cursor.close()

        return result

    # user数据库查询一条数据，返回字典列表
    def selectOne_user(self,sql):
        cursor =self.baseDB_conn().cursor()
        cursor.execute(sql)
        result=cursor.fetchone()
        cursor.close()
        return result

    # user数据库查询多条数据，返回字典列表
    def selectMany_user(self,sql,size):
        cursor =self.baseDB_conn().cursor()
        cursor.execute(sql)
        result=cursor.fetchmany(size)
        cursor.close()
        return result

    # user数据库查询多条数据，返回字典列表
    def selectAll_user(self,sql):
        cursor =self.baseDB_conn().cursor()
        cursor.execute(sql)
        result=cursor.fetchmall()
        cursor.close()
        return result


if __name__=="__main__":
    dbUtill1 =dbUtil()
    result= dbUtill1.selectOne_base("select * from alarm_add_data")
    print (result)