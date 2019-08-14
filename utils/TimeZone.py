# __*__coding=utf-8__*__
# autor  张鹏
# date 2018/09/11
# describe  班组时间

from utils.read_config import ReadCfgFile
from pyrest.cim_api import cim_api , user_cim_api ,dataService_interface
from  datetime import timedelta,datetime
import copy
from dateutil.relativedelta import relativedelta
from utils.db_util import DBHelper
import sys
from utils.format import floatFormat
endpoint_os_ues_web = ReadCfgFile('os_ues_cfg.ini').get_val('rest_os_ues_api', 'endpoint_os_web1')    #测试接口
cim_interface=ReadCfgFile('os_ues_cfg.ini').get_val('rest_support_api', 'cim_web_interface')  #cim接口
data_service=ReadCfgFile('os_ues_cfg.ini').get_val('rest_support_api', 'data_service_web')  #dataservice 接口
user_cim=ReadCfgFile('os_ues_cfg.ini').get_val('rest_support_api', 'user_cim_interface')
dataDB=eval(ReadCfgFile().get_val('database', '21_dataDB'))
LASTYEAR = ((datetime.now() - relativedelta(years=+1))+timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
TODAYBEGIN = datetime.now().strftime('%Y-%m-%d 00:00:00')
TODAYEND = datetime.now().strftime('%Y-%m-%d 23:59:59')
LASTMONTH = (datetime.now() - relativedelta(months=+1)).strftime('%Y-%m-%d %H:%M:%S')
NOW=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
nowHour=datetime.now().hour

class TimeZone():
    def __init__(self,):
        self.os_ues = eval(ReadCfgFile().get_val('database', 'os_ues'))

    def getDateTime24H(self,payload):#返回统计时间   payload={"isTeam":1,"stationId":"CA01ES01","startTime":"","endTime": "",}  #如果处在isTeam且为1，则取班组时间。如果startTime和endTime存在且值不为空，则取设置好的值。如果isTeam，startTime，endTime均无效，则取过去一年到当前的时间

        dateRange={}
        if 'isTeam' in payload.keys() and payload['isTeam'] ==1: #按照班组时间
            dateRange=self.getTeamTime24H(payload['stationId'])

        else: #不按照班组时间
            if 'startTime'in payload.keys() and 'endTime' in payload.keys() and payload['startTime'] != '' and  payload['startTime'] !='':  #如果参数中有起止时间，则取系统给定的时间
                dateRange['startTime']=payload['startTime']
                dateRange['endTime']=payload['endTime']

            else: #不输时间，起始为当前时间，结束时间往前推一年
                dateRange['startTime'] =LASTYEAR
                dateRange['endTime'] = NOW
        return dateRange

    def getTeamTime24H(self,stationId): #根据当前时间返回一天的班组时间
        sql = (
            "SELECT t.stage_one FROM pub_energy_stage t WHERE t.station_id = '{stationId}' AND t.energy_type = 'T'".format(
                stationId=stationId))
        DBHelper1 = DBHelper(self.os_ues, resultType='list')
        timeZone_list = DBHelper1.fetchAll(sql)
        if len(timeZone_list) > 1:
            print('班组时间配置有误')
            sys.exit(0)

        elif len(timeZone_list) < 1:  # 未设置班组时间，默认为{\n   "start": "08:00",\n   "end": "20:00"\n}, {\n   "start": "20:00",\n   "end": "08:00"\n}
            print('未设置班组时间')
            firstStage = {'start': '08:00', 'end': '20:00'}
            secondStage = {'start': '20:00', 'end': '08:00'}
            teamTimeRange = self.judgeTeamTime24H(firstStage, nowHour)
        else:
            teamTimeZone = eval(timeZone_list[0][0])
            print(teamTimeZone)

            minStart={}
            for item in teamTimeZone: #找到一天的开始时间
                if not minStart :
                    minStart=item
                else:
                    if int(item['start'].split(':')[0])<int(minStart['start'].split(':')[0]):
                        minStart=item
                    else:
                        minStart=minStart
            teamTimeRange=self.judgeTeamTime24H(minStart,nowHour)
        return  teamTimeRange

    def judgeTeamTime24H(self,firstStage,nowHour): #根据当前时间返回24小时区间
        teamTimeStage={}
        if int(firstStage['start'].split(':')[0])<=nowHour: #第一阶梯的开始时间小于当前时间
            teamTimeStage['startTime']=(datetime.now().replace(hour=int(firstStage['start'].split(':')[0]),minute=int(firstStage['start'].split(':')[1]),second=0)).strftime('%Y-%m-%d %H:%M:%S')
            teamTimeStage['endTime'] = ((datetime.now()+timedelta(days=1)).replace(hour=int(firstStage['start'].split(':')[0]), minute=int(firstStage['start'].split(':')[1]),second=0)).strftime('%Y-%m-%d %H:%M:%S')
        elif 0<=nowHour<int(firstStage['start'].split(':')[0]):#当前时间为0点以后，且小于第一阶梯的开始时间

            teamTimeStage['startTime'] = ((datetime.now()-timedelta(days=1)).replace(hour=int(firstStage['start'].split(':')[0]), minute=int(firstStage['start'].split(':')[1]),second=0)).strftime('%Y-%m-%d %H:%M:%S')
            teamTimeStage['endTime'] = (datetime.now() .replace(hour=int(firstStage['start'].split(':')[0]), minute=int(firstStage['start'].split(':')[1]),second=0)).strftime('%Y-%m-%d %H:%M:%S')
        else:
            print('班组时间第二阶段设置错误')
        return teamTimeStage

    def getDateTime(self,payload):#返回当前班组时间  payload={"isTeam":1,"stationId":"CA01ES01","startTime":"","endTime": "",}  #如果处在isTeam且为1，则取班组时间。如果startTime和endTime存在且值不为空，则取设置好的值。

        dateRange={}
        if 'isTeam' in payload.keys() and payload['isTeam'] ==1: #按照班组时间
            dateRange=self.getTeamTime(payload['stationId'])

        else: #不按照班组时间
            if 'startTime'in payload.keys() and 'endTime' in payload.keys() and payload['startTime'] != '' and  payload['startTime'] !='':  #如果参数中有起止时间，则取系统给定的时间
                dateRange['startTime']=payload['startTime']
                dateRange['endTime']=payload['endTime']

            else: #不输时间，起始为当前时间，结束时间往前推一年
                dateRange['startTime'] =LASTYEAR
                dateRange['endTime'] = NOW
        return dateRange

    def getTeamTime(self,stationId):
        teamTimeStage={}
        sql=("SELECT t.stage_one FROM pub_energy_stage t WHERE t.station_id = '{stationId}' AND t.energy_type = 'T'".format(stationId=stationId))
        DBHelper1=DBHelper(self.os_ues,resultType='list')
        timeZone_list=DBHelper1.fetchAll(sql)
        if len(timeZone_list)>1:
            print('班组时间配置有误')
            sys.exit(0)

        elif len(timeZone_list)<1: #未设置班组时间，默认为{\n   "start": "08:00",\n   "end": "20:00"\n}, {\n   "start": "20:00",\n   "end": "08:00"\n}
            print('未设置班组时间')
            firstStage={'start': '08:00', 'end': '20:00'}
            secondStage={'start':'20:00', 'end': '08:00'}

            if int(firstStage['start'].split(':')[0]) <= nowHour < int(
                    firstStage['end'].split(':')[0]):  # 如果当前时间的小时在第一阶梯之间
                teamTimeStage['startTime'] = (datetime.now().replace(hour=int(firstStage['start'].split(':')[0]),
                                                                     minute=int(firstStage['start'].split(':')[1]),
                                                                     second=0)).strftime('%Y-%m-%d %H:%M:%S')
                teamTimeStage['endTime'] = (datetime.now().replace(hour=int(firstStage['end'].split(':')[0]),
                                                                   minute=int(firstStage['end'].split(':')[1]),
                                                                   second=0)).strftime('%Y-%m-%d %H:%M:%S')
            else:  # 当前时间的小时不在第一阶梯则取第二阶梯

                teamTimeStage = self.judgeTeamTime(secondStage, nowHour)

        else: #获取班组时间
            teamTimeZone=eval(timeZone_list[0][0])
            print(teamTimeZone)
            for item in teamTimeZone:
                if int(item['start'].split(':')[0]) <int(item['end'].split(':')[0] ): #如果该时间段起始时间小于结束时间
                    if int(item['start'].split(':')[0]) <=nowHour<int(item['end'].split(':')[0] ):#如果当前时间大于起始时间小于结束时间
                        teamTimeStage['startTime'] = (
                            datetime.now().replace(hour=int(item['start'].split(':')[0]),
                                                   minute=int(item['start'].split(':')[1]), second=0)).strftime(
                            '%Y-%m-%d %H:%M:%S')
                        teamTimeStage['endTime'] = (datetime.now().replace(hour=int(item['end'].split(':')[0]),
                                                                           minute=int(item['end'].split(':')[1]),
                                                                           second=0)).strftime('%Y-%m-%d %H:%M:%S')
                        return teamTimeStage
                elif int(item['start'].split(':')[0]) >int(item['end'].split(':')[0] ):
                    teamTimeStage = self.judgeTeamTime(item, nowHour)
                    return teamTimeStage
                else: #起始时间等于开始时间
                    teamTimeStage['startTime'] = (
                        datetime.now().replace(hour=int(item['start'].split(':')[0]),
                                               minute=int(item['start'].split(':')[1]), second=0)).strftime(
                        '%Y-%m-%d %H:%M:%S')
                    teamTimeStage['endTime'] = ((datetime.now()+timedelta(days=1)).replace(hour=int(item['end'].split(':')[0]),
                                                                       minute=int(item['end'].split(':')[1]),
                                                                       second=0)).strftime('%Y-%m-%d %H:%M:%S')
                    return teamTimeStage


    def judgeTeamTime(self,timeStage,nowHour): #根据当前时间返回对应的班组显示时间(第二阶梯)
        teamTimeStage={}
        if int(timeStage['start'].split(':')[0])<=nowHour<24: #当前时间为24点以前
            teamTimeStage['startTime']=(datetime.now().replace(hour=int(timeStage['start'].split(':')[0]),minute=int(timeStage['start'].split(':')[1]),second=0)).strftime('%Y-%m-%d %H:%M:%S')
            teamTimeStage['endTime'] = ((datetime.now()+timedelta(days=1)).replace(hour=int(timeStage['end'].split(':')[0]), minute=int(timeStage['end'].split(':')[1]),second=0)).strftime('%Y-%m-%d %H:%M:%S')
        elif 0<=nowHour<int(timeStage['end'].split(':')[0]):#当前时间为0点以后

            teamTimeStage['startTime'] = ((datetime.now()-timedelta(days=1)).replace(hour=int(timeStage['start'].split(':')[0]), minute=int(timeStage['start'].split(':')[1]),second=0)).strftime('%Y-%m-%d %H:%M:%S')
            teamTimeStage['endTime'] = (datetime.now() .replace(hour=int(timeStage['end'].split(':')[0]), minute=int(timeStage['end'].split(':')[1]),second=0)).strftime('%Y-%m-%d %H:%M:%S')
        else:
            print('班组时间第二阶段设置错误')
        return teamTimeStage

class TimeUtil(): #时间处理类

    def timeDif(self,startTime,endTime): #计算时间差，返回差的秒数
        startTime=datetime.strptime(startTime,'%Y-%m-%d %H:%M:%S')
        endTime=datetime.strptime(endTime,'%Y-%m-%d %H:%M:%S')
        dif=endTime-startTime
        return dif.days
        #print(endTime1)



if __name__=='__main__':
    # TimeZone1=TimeZone()
    #
    # Time_payload={"isTeam":1,"stationId":"CA16ES01","startTime":"2016-08-18 14:29:28","endTime": "2018-08-18 14:29:28",}
    # print(TimeZone1.getDateTime24H(Time_payload))

    TimeUtil1=TimeUtil()
    print(TimeUtil1.timeDif('2016-08-18 14:29:28','2016-08-20 14:29:27'))