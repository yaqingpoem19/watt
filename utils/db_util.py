# __*__coding=utf-8__*__
# autor 张鹏
# date  2018/07/16
# describe  数据库连接类
import pymysql
import logging
import sys
from utils.read_config import ReadCfgFile
from pymysql import DatabaseError ,MySQLError
import psycopg2

# 加入日志
# 获取logger实例
logger = logging.getLogger("baseSpider")
# 指定输出格式
formatter = logging.Formatter(' \033[1;30;46m %(asctime)s\ %(levelname)-8s:%(message)s')

# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# 为logge添加具体的日志处理器
logger.addHandler(console_handler)

logger.setLevel(logging.INFO)

class DBHelper(object):
    # 构造函数
    def __init__(self,args,resultType=None,):

        if resultType=='list':
            cursorclass=pymysql.cursors.Cursor
        else:
            cursorclass = pymysql.cursors.DictCursor

        self.args=args
        try:
            self.conn = pymysql.connect(cursorclass=cursorclass,charset='utf8',**self.args)
        except (DatabaseError, MySQLError) as e:
            error = 'MySQL execute failed! ERROR (%s): %s' % (e.args[0], e.args[1])
            logger.error(error)
        self.cur = self.conn.cursor()


    # 关闭数据库
    def close(self):
        # 如果数据打开，则关闭；否则没有操作
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
        return True

    # 执行数据库的sq语句,主要用来做插入操作
    def execute(self, sql):
        try:
            if self.conn and self.cur:
                # 正常逻辑，执行sql，提交操作
                self.cur.execute(sql)
                logger.info('sql:{sql}'.format(sql=sql).format(sql=sql))
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logger.error("execute failed: " + sql)
            error='MySQL execute failed! ERROR (%s): %s' % (e.args[0], e.args[1])
            logger.error(error)
            self.close()
            return False
        return True


    def insert(self, sql):
        try:
            if self.conn and self.cur:
                # 正常逻辑，执行sql，提交操作
                self.cur.execute(sql)
                logger.info('sql:{sql}'.format(sql=sql))
                self.lastRowId=int(self.cur.lastrowid)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            error = 'MySQL execute failed! ERROR (%s): %s' % (e.args[0], e.args[1])
            logger.error(error)
            self.close()
            return False
        return True

    # 用来查询表数据
    def fetchAll(self, sql):
        self.execute(sql)
        return self.cur.fetchall()

    def fetchOne(self,sql):
        # 取得上个查询的结果，是单个结果
        self.execute(sql)
        return self.cur.fetchone()

    # base数据库查询多条数据，返回字典列表
    def fetchMany(self, sql,size):
        self.execute(sql)

        return self.cur.fetchmany(size)
#PG数据库连接
class DBhelper_ps():
    def __init__(self,args):
        self.conn = psycopg2.connect(database=args['database'], user=args['user'], password=args['user'], host=args['host'], port='5432')
        self.cur = self.conn.cursor()


    def selectAll(self,sql):
        self.cur.execute(sql)
        # 获取表的所有字段名称
        coloumns = [row[0] for row in self.cur.description]
        result = [[str(item) for item in row] for row in self.cur.fetchall()]
        return [dict(zip(coloumns, row)) for row in result]

if __name__ == '__main__':
    base_ku1 = eval(ReadCfgFile().get_val('database', 'base_ku1'))
    da=DBHelper(base_ku1,resultType='')
    sql ="select * from alarm_add_data where add_data_id =110008";

    print(da.fetchOne(sql))

