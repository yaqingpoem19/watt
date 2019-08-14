# __*__coding=utf-8__*__
# autor  张鹏
# date   2018/08/17
# describe  散点图工具类
from utils.read_config import ReadCfgFile
from pyrest.cim_api import cim_api , user_cim_api ,dataService_interface
from  datetime import timedelta,datetime
import copy
from dateutil.relativedelta import relativedelta
from utils.db_util import DBHelper
import sys
from utils.format import floatFormat
from utils.TimeZone import  TimeUtil
import calendar

endpoint_os_ues_web = ReadCfgFile('os_ues_cfg.ini').get_val('rest_os_ues_api', 'endpoint_os_web1')    #测试接口
cim_interface=ReadCfgFile('os_ues_cfg.ini').get_val('rest_support_api', 'cim_web_interface')  #cim接口
data_service=ReadCfgFile('os_ues_cfg.ini').get_val('rest_support_api', 'data_service_web')  #dataservice 接口
user_cim=ReadCfgFile('os_ues_cfg.ini').get_val('rest_support_api', 'user_cim_interface')
dataDB=eval(ReadCfgFile().get_val('database', '21_dataDB'))
os_data=eval(ReadCfgFile().get_val('database', 'os_data'))
LASTYEAR = ((datetime.now() - relativedelta(years=+1))+timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
TODAYBEGIN = datetime.now().strftime('%Y-%m-%d 00:00:00')
TODAYEND = datetime.now().strftime('%Y-%m-%d 23:59:59')
LASTMONTH = (datetime.now() - relativedelta(months=+1)).strftime('%Y-%m-%d %H:%M:%S')
LASTMONTH1 = (datetime.now() - relativedelta(months=+1)).strftime('%Y-%m')
NOW=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
nowHour=datetime.now().hour


class EfficiencyAnyalysisDetails():

    def __init__(self,):
        self.startTime=''
        self.pointLfs = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        self.cim=cim_api(cim_interface)
        self.os_ues = eval(ReadCfgFile().get_val('database', 'os_ues'))
        self.data_service_interface = dataService_interface(data_service)
        self.time_zone=TimeZone()

    #获取每个月概率最大的3个点
    def getMaxProbability(self,payload):
        TimeUtil1=TimeUtil()
        montheList=TimeUtil1.create_month_list(endMonth=LASTMONTH1,space=11)

        tempResultList=[]
        for month in montheList:
            tempResult = {}
            monthSanDianList=[]
            tempResult['dateYm']=month
            startTime =month + '-01 00:00:00'
            firstDayWeekDay, monthRange=calendar.monthrange(datetime.strptime(month,'%Y-%m').year,datetime.strptime(month,'%Y-%m').month)
            #print(monthRange)
            endTime=month +'-'+ str(monthRange) + ' 23:59:59'
            sanDianPayload=payload
            sanDianPayload['startTime']=startTime
            sanDianPayload['endTime']=endTime
            sanDianResult=Eff.EfficiencyAnyalysisDetails(sanDianPayload)
            for deviceSanDian in sanDianResult:
                sanDianDict={}
                code=list(deviceSanDian.keys())[0]
                sanDianList=deviceSanDian[code]['pointCounts']
                sanDianDict['code']=code
                sanDianDict['sanDianList']=sanDianList
                monthSanDianList.append(sanDianDict)

            tempResult['monthSanDianList']=monthSanDianList
            tempResultList.append(tempResult)
        #print(tempResultList)
        allDeviceSanDian=[]
        for device in payload['deviceIds'] :
            deviceSanDianDict={} #每个设备的散点
            deviceSanDianDict['code']=device['deviceId']
            sanDianList=[] #接收每个月的散点数据
            for itemResult in tempResultList:
                monthSanDian={} #单月的散点数据
                monthSanDian['dateYm']=itemResult['dateYm']
                monthSanDian['sanDian']= list(map(lambda x :x['sanDianList'],list(filter(lambda x:x['code']==device['deviceId'],itemResult['monthSanDianList']))))[0]
                sanDianList.append(monthSanDian)
            deviceSanDianDict['monthSanDian'] =sanDianList
            allDeviceSanDian.append(deviceSanDianDict)
        for item in allDeviceSanDian:
            self.getTop3AndIndex(item['monthSanDian'])
        #print(allDeviceSanDian)

    def getTop3AndIndex(self,monthSanDian):

        massPointsList=[]
        for tempMonthSanDian in  monthSanDian:
            massPointsDict = {}
            massPointsDict['dateYm']=tempMonthSanDian['dateYm']
            if tempMonthSanDian['sanDian'] :
                top3List=tempMonthSanDian['sanDian']
                massPointsDict['massPoints']=self.getMax3value(top3List)

            else:
                top3List = []
                massPointsDict['massPoints']=top3List

            massPointsList.append(massPointsDict)
        print(massPointsList)

    #获取最大的3个值和坐标
    def getMax3value(self,massPoints):
        massPintsList=[]
        massPointsIndex=[]
        maxValue=0
        maxIndex=0
        secondValue=0
        secondIndex = 0
        thridValue=0
        thridIndex = 0
        coordLenth=0
        for item in massPoints:
            coordLenth=len(item)
            massPintsList+=item
        for index in range(0,len(massPintsList)):
            if massPintsList[index] =='-':
                maxValue=maxValue
            else:
                if maxValue>=float(massPintsList[index]):
                    maxValue=maxValue
                else:
                    maxValue=float(massPintsList[index])
                    maxIndex=index

        for index in range(0,len(massPintsList)):
            if massPintsList[index] =='-' or index == maxIndex:
                secondValue=secondValue
            else:
                if secondValue>=float(massPintsList[index]):
                    secondValue=secondValue
                else:
                    secondValue=float(massPintsList[index])
                    secondIndex=index

        for index in range(0,len(massPintsList)):
            if massPintsList[index] =='-' or index == maxIndex or index ==secondIndex:
                secondValue=secondValue
            else:
                if thridValue>=float(massPintsList[index]):
                    thridValue=thridValue
                else:
                    thridValue=float(massPintsList[index])
                    thridIndex=index

        # print(coordLenth)
        # print(massPintsList)

        # print(maxValue)
        # print(maxIndex)
        maxLoadRateIndex=(maxIndex+1)//coordLenth
        maxComsumeIndex=(maxIndex+1)%coordLenth
        # print(maxLoadRateIndex)
        # print(maxComsumeIndex)
        maxIndexValue={'rateCount':maxValue,'maxLoadRateIndex':maxLoadRateIndex,'maxComsumeIndex':maxComsumeIndex}


        # print(secondValue)
        # print(secondIndex)
        secondLoadRateIndex = (secondIndex + 1) // coordLenth
        secondComsumeIndex = (secondIndex + 1) % coordLenth
        # print(secondLoadRateIndex)
        # print(secondComsumeIndex)
        secondIndexValue={'rateCount':secondValue,'secondLoadRateIndex':secondLoadRateIndex,'secondComsumeIndex':secondComsumeIndex}

        # print(thridValue)
        # print(thridIndex)
        thridLoadRateIndex = (thridIndex + 1) // coordLenth
        thridComsumeIndex = (thridIndex + 1) % coordLenth
        # print(thridLoadRateIndex)
        # print(thridComsumeIndex)
        thridIndexValue={'rateCount':thridValue,'thridLoadRateIndex':thridLoadRateIndex,'thridComsumeIndex':thridComsumeIndex}
        massPointsIndex.append(maxIndexValue)
        massPointsIndex.append(secondIndexValue)
        massPointsIndex.append(thridIndexValue)

        return massPointsIndex



    #设备散点图分析-按月统计分析(能效良好)
    def copGoodInMonth(self,payload):
        startDate=datetime.now().strftime('%Y-%m-01')
        #print(startDate)
        endDate=datetime.now().strftime('%Y-%m-%d')
        TimeUtil1=TimeUtil()
        timeList=TimeUtil1.create_assist_date(startDate,endDate)
        massPointDtoDict={}
        analysisByMonth=[]
        goodNumTotal=0
        for time in timeList:
            analysisDay={}
            startTime=time + ' 00:00:00'
            endTime=time+ ' 23:59:59'
            Calendars=self.copGoodAnalysisCalendars(payload,startTime,endTime)
            analysisDay['dateYmd']=time
            massPoints=[]
            for tmpCalender in Calendars:
                if tmpCalender['stateCode']==2:  #如果状态为良好
                    goodNumTotal+=1
                    tempMassPoint={}
                    time=datetime.strptime(tmpCalender['time'],'%Y-%m-%d %H:%M:%S').strftime('%H:%M')
                    dataDetails=tmpCalender['dataDetails'][0]
                    loadRate=dataDetails['lf']
                    comsume=dataDetails['uec']
                    tempMassPoint['time']=time
                    tempMassPoint['loadRate']=loadRate
                    tempMassPoint['comsume'] = comsume
                    massPoints.append(tempMassPoint)
            analysisDay['massPoints']=massPoints
            analysisByMonth.append(analysisDay)
        analysisByMonth = list(filter(lambda x: len(x['massPoints']) != 0, analysisByMonth))
        massPointDtoDict['goodNumTotal'] =goodNumTotal
        massPointDtoDict['analysisByMonth']=analysisByMonth


        #print(massPointDtoDict)
        return massPointDtoDict

    def copGoodAnalysisCalendars(self,payload,startTime=None,endTime=None):
        statues_code = {0: '异常', -1: '-', 2: '良好', 1: '正常'}
        statues = self.currentPoints(payload,False,startTime,endTime)  # 获取当前状态结果
        timeList = list(map(lambda x: x['time'], statues[0]))
        # print(timeList)
        temp_resultList = []
        for time in timeList:
            tempStatus = {}
            tempStatus['time'] = time
            temp = []
            for item in statues:
                temp.append(list(filter(lambda x: x['time'] == time, item))[0])

                tempStatus['data'] = temp

            temp_resultList.append(tempStatus)

        # print(temp_resultList)
        result = []
        for item in temp_resultList:
            temp = {}
            temp['time'] = item['time']
            temp['dataDetails'] = item['data']
            statues_list = list(map(lambda x: x['statusCode'], item['data']))

            if 0 in statues_list:
                stateCode = 0
            else:
                if 2 in statues_list:
                    stateCode = 2
                else:
                    if 1 in statues_list:
                        stateCode = 1
                    else:
                        stateCode = -1
            temp['stateCode'] = stateCode
            temp['state'] = statues_code[stateCode]
            result.append(temp)
        #print(result)
        return result

    # 生成日历图
    def analysisCalendars (self,payload):
        statues_code={0:'异常',-1:'-',2:'良好',1:'正常'}
        statues=self.currentPoints(payload) #获取当前状态结果
        timeList = list(map(lambda x: x['time'], statues[0]))
        #print(timeList)
        temp_resultList=[]
        for time in timeList:
            tempStatus={}
            tempStatus['time'] =time
            temp=[]
            for item in statues:
                temp.append(list( filter(lambda x:  x['time']==time,item))[0])

                tempStatus['data']=temp

            temp_resultList.append(tempStatus)

        #print(temp_resultList)
        result=[]
        for item in temp_resultList:
            temp={}
            temp['time']=item['time']
            temp['dataDetails']=item['data']
            statues_list=list(map(lambda x:x['statusCode'],item['data']))

            if 0 in statues_list:
                stateCode=0
            else:
                if 2 in statues_list:
                    stateCode=2
                else:
                    if 1 in statues_list:
                        stateCode=1
                    else:
                        stateCode=-1
            temp['stateCode']=stateCode
            temp['state']=statues_code[stateCode]
            result.append(temp)
        #print(result)
        return result



    def currentPoints(self,payload,isCalendar=True,startTime=None,endTime=None):#当天的设备状态判断,如果传入isteam则当天时间取班组时间，如果传入开始时间和结束时间，则散点按照开始结束时间统计，如果不传默认按1年时间统计
        # 首先判断传入时间，是否为班组，或者默认时间
        time_payload = {'stationId': payload['stationId']}
        time_zone = {}
        if 'isTeam' in payload.keys() and payload['isTeam'] == 1:  # 如果参数中传入isTeam并且值为1，则取班组时间
            time_payload['isTeam'] = payload['isTeam']
            time_zone = self.time_zone.getDateTime(time_payload)
        elif isCalendar == False: #如果不是日历图
            time_zone['startTime'] = startTime
            time_zone['endTime'] = endTime

        else:  # 否则取0-23点时间
            time_zone['startTime'] = TODAYBEGIN
            time_zone['endTime'] = TODAYEND

        if 'deviceIds' in payload.keys(): #设备散点图分析
            EfficiencyAnyalysisDetails_payload = {'stationId': payload['stationId'], 'deviceIds': payload['deviceIds']}
            if 'startTime' in payload.keys() and 'endTime' in payload.keys():
                EfficiencyAnyalysisDetails_payload['startTime'] = payload['startTime']
                EfficiencyAnyalysisDetails_payload['endTime'] = payload['endTime']
            sanDianList=self.EfficiencyAnyalysisDetails(EfficiencyAnyalysisDetails_payload)
            #print(sanDianList)
            statues=self.getReferenceValue(payload['deviceIds'],sanDianList,time_zone,payload['stationId'])
        elif 'systems' in payload.keys() :   #系统当天时间分析
            EfficiencyAnyalysisDetails_payload = {'stationId': payload['stationId'], 'systems': payload['systems']}
            if 'startTime' in payload.keys() and 'endTime' in payload.keys():
                EfficiencyAnyalysisDetails_payload['startTime'] = payload['startTime']
                EfficiencyAnyalysisDetails_payload['endTime'] = payload['endTime']
            sanDianList = self.EfficiencyAnyalysisDetails(EfficiencyAnyalysisDetails_payload)
            # print(sanDianList)
            #statues=self.currentStatusjudge(payload['systems'], sanDianList, time_zone,payload['stationId'])
            statues=self.getReferenceValue(payload['systems'], sanDianList, time_zone,payload['stationId'])
        #print(statues)
        return statues
    def getReferenceValue(self,sysList,sanDianList,time_zone,stationId): #获取基准值
        DBHelper1=DBHelper(os_data,'list')
        #获取checkPoint
        checkPoint=''
        for device_list in sysList:
            if 'deviceId' in device_list.keys(): #设备分析
                checkPoint = self.getDeviceCheckPoint(device_list['deviceId']).split(',')[0]
            else:#系统分析
                checkPoint = self.getSystemCheckPoint(device_list['sysId'],device_list['sysType'],stationId).split(',')[0]
        #print(checkPoint)
        sql=("select t.datum_value from bas_datum t where t.project_id ='{stationId}'  and t.`code`='{checkPoint}'".format(stationId=stationId,checkPoint=checkPoint))
        referenceValue=DBHelper1.fetchOne(sql)
        if referenceValue : #如果不为空
            res=self.currentStatusjudgeDepondOnReferenceValue(sysList,sanDianList,time_zone,stationId,referenceValue)
        else:
            res=self.currentStatusjudge(sysList,sanDianList,time_zone,stationId)

        return res


    #判断基准值日历图
    def currentStatusjudgeDepondOnReferenceValue(self,sysList,sanDianList,time_zone,stationId,ReferenceValue):
        statues_code={0:'异常',-1:'-',2:'良好',1:'正常'}
        #ReferenceValue=self.getReferenceValue(sysList,stationId)
        ReferenceValue=ReferenceValue[0]
        result_list = []
        for device_list in sysList:
            if 'deviceId' in device_list.keys():  # 设备分析
                checkPoint = self.getDeviceCheckPoint(device_list['deviceId'])
                sanDian = list(filter(lambda x: device_list['deviceId'] in x.keys(), sanDianList))[0][
                    device_list['deviceId']]
                code = device_list['deviceId']
            else:  # 系统分析
                checkPoint = self.getSystemCheckPoint(device_list['sysId'], device_list['sysType'], stationId)

                sanDian = list(filter(lambda x: device_list['sysId'] in x.keys(), sanDianList))[0][
                    device_list['sysId']]
                code = device_list['sysId']

            fact_data = self.requestDataService(stationId, checkPoint, time_zone)  # 获取当天的事实数据

            LF_list = list(filter(lambda x: x['code'].endswith('LF'), fact_data))[0]['datas']  # 负荷率散点
            # print(LF_list)
            LF_list=list(map(lambda x :{'value':float(floatFormat(x['value'],3)),'col_time':x['col_time'] } if x['value'] != '' else {'value':'','col_time':x['col_time']},LF_list))
            uec_list = list(filter(lambda x: not x['code'].endswith('LF'), fact_data))[0]['datas']  # 能效或单耗散点
            uec_list = list(map(lambda x :{'value':float(floatFormat(x['value'],3)),'col_time':x['col_time'] } if x['value'] != '' else {'value':'','col_time':x['col_time']},uec_list))
            pointMaxWithLF_value = sanDian['pointMaxWithLF_value']  # 获取按照lf统计，每个lf区间上对应的cop的最大区间
            # print(LF_list)
            # print('-' * 50)
            # print(uec_list)
            # print('*'*50)
            #当天数据过滤
            for lf, uec in zip(LF_list, uec_list):
                if lf['value']=='' or uec['value']=='' :# 如果同一时间负荷率与单耗有一个值为空，则将两个值均置为'-'
                    lf['value'] = uec['value'] = '-'
                else:
                    if (float(lf['value']) <5 and  float(uec['value'])== 0) :  # 如果同一时间负荷率的值小于5且单耗的值均为0，则将两个值均置为'-'
                        lf['value'] = uec['value'] = '-'
            # print('#############################################')
            # print(LF_list)
            # print(uec_list)
            # print('#############################################')
            result_temp_list = []
            for corrent_lf in LF_list:  # 循环当天的负荷率
                corrent_result = {}  # 接收结果数据
                for lf_index, uecRange in zip(range(0, len(self.pointLfs)), pointMaxWithLF_value):
                    #statues = 0  # 当前系统状态，1为good，-1为abnormal，0为 normal
                    statusCode = 1
                    corrent_uec = list(filter(lambda x: x['col_time'] == corrent_lf['col_time'], uec_list))[0]  # 当前时刻的uec数据
                    if lf_index == 0:  # 如果是第一个负荷率的值
                        if corrent_lf['value'] is not None and corrent_lf['value'] != '-':
                            if 0 <= float(corrent_lf['value']) < self.pointLfs[lf_index]:  # 如果当天的负荷率大于0 ，小于第一个值
                                # 判断uec的返回
                                if float(corrent_uec['value'])>ReferenceValue :#如果uec的值大于基准值，状态为异常
                                    #statues = -1
                                    statusCode = 0
                                else:
                                    if len(uecRange) == 2:  # 如果uecRange是一个区间
                                        if uecRange[0] <= float(corrent_uec['value']) < uecRange[1]:  # 如果uec的值在最大值之间，则正常
                                            #statues = 0
                                            statusCode= 1
                                        elif uecRange[1] <= corrent_uec['value']:  # 如果当前的值大于较大值。则异常：
                                            #statues = -1
                                            statusCode = 0
                                        else:  # 如果当前值小于较小的值，则为良好
                                            #statues = 1
                                            statusCode = 2
                                    elif len(uecRange) == 1:  # 如果uecRange只有一个值
                                        if uecRange[0] <= corrent_uec['value']:  # 如果大于该值，正运行良好
                                            #statues = 0
                                            statusCode=1
                                        else:  # 否则运行良好
                                            statusCode = 2
                                corrent_result['code'] = code
                                corrent_result['statusCode'] = statusCode
                                corrent_result['status']=statues_code[statusCode]
                                corrent_result['lf'] = corrent_lf['value']
                                corrent_result['uec'] = corrent_uec['value']
                                corrent_result['time'] = corrent_lf['col_time']

                        else:
                            corrent_result['code'] = code
                            corrent_result['statusCode'] = -1
                            corrent_result['status'] = statues_code[-1]
                            corrent_result['lf'] = corrent_lf['value']
                            corrent_result['uec'] = corrent_uec['value']
                            corrent_result['time'] = corrent_lf['col_time']
                    elif 0 < lf_index < len(self.pointLfs) - 1:  # 当纵做在2-9 之间
                        if corrent_lf['value'] is not None and corrent_lf['value'] != '-':
                            if self.pointLfs[lf_index - 1] <= float(corrent_lf['value']) < self.pointLfs[
                                lf_index]:  # 如果当天的负荷率大于前一个值 ，小于当前值
                                # 判断uec的返回
                                if float(corrent_uec['value'])>ReferenceValue :#如果uec的值大于基准值，状态为异常
                                    #statues = -1
                                    statusCode=0
                                else:
                                    if len(uecRange) == 2:  # 如果uecRange是一个区间
                                        if uecRange[0] <= corrent_uec['value'] < uecRange[1]:  # 如果uec的值在最大值之间
                                            #statues = 0
                                            statusCode=1
                                        elif uecRange[1] <= corrent_uec['value']:  # 如果当前的值大于较大值，则异常：
                                            #statues = -1
                                            statusCode=0
                                        else:  # 如果当前值小于较小的值，则为良好
                                            #statues = 1
                                            statusCode=2
                                    elif len(uecRange) == 1:  # 如果uecRange只有一个值
                                        if uecRange[0] <= corrent_uec['value']:  # 如果大于该值，正运行良好
                                            #statues = 0
                                            statusCode=1
                                        else:  # 否则运行良好
                                            #statues = 1
                                            statusCode=2
                                corrent_result['code'] = code
                                corrent_result['statusCode'] = statusCode
                                corrent_result['status'] = statues_code[statusCode]
                                corrent_result['lf'] = corrent_lf['value']
                                corrent_result['uec'] = corrent_uec['value']
                                corrent_result['time'] = corrent_lf['col_time']

                        else:
                            corrent_result['code'] = code
                            corrent_result['statusCode'] = -1
                            corrent_result['status'] = statues_code[-1]
                            corrent_result['lf'] = corrent_lf['value']
                            corrent_result['uec'] = corrent_uec['value']
                            corrent_result['time'] = corrent_lf['col_time']
                    elif lf_index == len(self.pointLfs) - 1:  # 如果是最后一个值
                        if corrent_lf['value'] is not None and corrent_lf['value'] != '-':
                            if self.pointLfs[lf_index - 1] <= float(corrent_lf['value']):  # 如果当天的负荷率大于前一个值 ，小于当前值
                                # 判断uec的返回
                                if float(corrent_uec['value'])>ReferenceValue :#如果uec的值大于基准值，状态为异常
                                    #statues = -1
                                    statusCode=0
                                else:
                                    if len(uecRange) == 2:  # 如果uecRange是一个区间
                                        if uecRange[0] <= corrent_uec['value'] < uecRange[1]:  # 如果uec的值在最大值之间
                                            #statues = 0
                                            statusCode=1
                                        elif uecRange[1] <= corrent_uec['value']:  # 如果当前的值大于较大值：
                                            #statues = -1
                                            statusCode=0
                                        else:  # 如果当前值小于较小的值，则为良好
                                            #statues = 1
                                            statusCode=2
                                    elif len(uecRange) == 1:  # 如果uecRange只有一个值
                                        if uecRange[0] <= corrent_uec['value']:  # 如果大于该值，正运行良好
                                            #statues = 0
                                            statusCode=1
                                        else:  # 否则运行良好
                                            #statues = 1
                                            statusCode=2
                                corrent_result['code'] = code
                                corrent_result['statusCode'] = statusCode
                                corrent_result['status'] = statues_code[statusCode]
                                corrent_result['lf'] = corrent_lf['value']
                                corrent_result['uec'] = corrent_uec['value']
                                corrent_result['time'] = corrent_lf['col_time']

                        else:
                            corrent_result['code'] = code
                            corrent_result['statusCode'] = -1
                            corrent_result['status'] = statues_code[-1]
                            corrent_result['lf'] = corrent_lf['value']
                            corrent_result['uec'] = corrent_uec['value']
                            corrent_result['time'] = corrent_lf['col_time']

                result_temp_list.append(corrent_result)
            result_list.append(result_temp_list)
        return result_list



    #未判断基准值日历图
    def currentStatusjudge(self,sysList,sanDianList,time_zone,stationId):
        statues_code = {0: '异常', -1: '-', 2: '良好', 1: '正常'}
        result_list=[]
        for device_list in sysList:
            if 'deviceId' in device_list.keys(): #设备分析
                checkPoint = self.getDeviceCheckPoint(device_list['deviceId'])
                sanDian = list(filter(lambda x: device_list['deviceId'] in x.keys(), sanDianList))[0][
                    device_list['deviceId']]
                code=device_list['deviceId']
            else:#系统分析
                checkPoint = self.getSystemCheckPoint(device_list['sysId'],device_list['sysType'],stationId)

                sanDian = list(filter(lambda x: device_list['sysId'] in x.keys(), sanDianList))[0][
                    device_list['sysId']]
                code=device_list['sysId']

            fact_data = self.requestDataService(stationId, checkPoint, time_zone)  # 获取当天的事实数据
            #print(fact_data)

            LF_list = list(filter(lambda x: x['code'].endswith('LF'), fact_data))[0]['datas']  # 负荷率散点
            LF_list=list(map(lambda x :{'value':float(floatFormat(x['value'],3)),'col_time':x['col_time'] } if x['value'] != '' else {'value':'','col_time':x['col_time']},LF_list))

            uec_list = list(filter(lambda x: not x['code'].endswith('LF'), fact_data))[0]['datas']  # 能效或单耗散点
            uec_list=list(map(lambda x :{'value':float(floatFormat(x['value'],3)),'col_time':x['col_time'] } if x['value'] != '' else {'value':'','col_time':x['col_time']},uec_list))

            LF_list=list(map(lambda x: {'value':x['value'],'col_time':x['col_time']} if x['col_time'] != datetime.now().strftime('%Y-%m-%d %H:00:00') else {'value':'','col_time':x['col_time']},LF_list))
            uec_list = list(map(lambda x: {'value': x['value'], 'col_time': x['col_time']} if x['col_time'] != datetime.now().strftime('%Y-%m-%d %H:00:00') else {'value': '', 'col_time': x['col_time']}, uec_list))
            pointMaxWithLF_value = sanDian['pointMaxWithLF_value']  # 获取按照lf统计，每个lf区间上对应的cop的最大区间
            # print(LF_list)
            # print('-' * 50)
            # print(uec_list)
            # print('*'*50)

            for lf, uec in zip(LF_list, uec_list):
                if lf['value']=='' or uec['value']=='' :# 如果同一时间负荷率与单耗有一个值为空，则将两个值均置为'-'
                    lf['value'] = uec['value'] = '-'
                else:
                    if (float(lf['value']) <5 and  float(uec['value'])== 0) :  # 如果同一时间负荷率的值小于5且单耗的值均为0，则将两个值均置为'-'
                        lf['value'] = uec['value'] = '-'
            # print('#############################################')
            # print(LF_list)
            # print(uec_list)
            # print('#############################################')
            result_temp_list = []
            for corrent_lf in LF_list:  # 循环当天的负荷率
                corrent_result = {}  # 接收结果数据
                for lf_index, uecRange in zip(range(0, len(self.pointLfs)), pointMaxWithLF_value):
                    #statues = 0  # 当前系统状态，1为good，-1为abnormal，0为 normal
                    statusCode=1
                    corrent_uec = list(filter(lambda x: x['col_time'] == corrent_lf['col_time'], uec_list))[0]  # 当前时刻的uec数据
                    #print(corrent_uec)
                    if lf_index == 0:  # 如果是第一个负荷率的值
                        if corrent_lf['value'] is not None and corrent_lf['value'] != '-':
                            if 0 <= float(corrent_lf['value']) < self.pointLfs[lf_index]:  # 如果当天的负荷率大于0 ，小于第一个值
                                # 判断uec的返回
                                if len(uecRange) == 2:  # 如果uecRange是一个区间
                                    if uecRange[0] <= float(corrent_uec['value']) < uecRange[1]:  # 如果uec的值在最大值之间，则正常
                                        #statues = 0
                                        statusCode=1
                                    elif uecRange[1] <= corrent_uec['value']:  # 如果当前的值大于较大值。则异常：
                                        #statues = -1
                                        statusCode=0
                                    else:  # 如果当前值小于较小的值，则为良好
                                        #statues = 1
                                        statusCode=2
                                elif len(uecRange) == 1:  # 如果uecRange只有一个值
                                    if uecRange[0] <= corrent_uec['value']:  # 如果大于该值，正运行良好
                                        #statues = 0
                                        statusCode=1
                                    else:  # 否则运行良好
                                        #statues = 1
                                        statusCode=2
                                corrent_result['code'] = code
                                corrent_result['statusCode'] = statusCode
                                corrent_result['status'] = statues_code[statusCode]
                                corrent_result['lf'] = corrent_lf['value']
                                corrent_result['uec'] = corrent_uec['value']
                                corrent_result['time'] = corrent_lf['col_time']

                        else:
                            corrent_result['code'] = code
                            corrent_result['statusCode'] = -1
                            corrent_result['status'] = statues_code[-1]
                            corrent_result['lf'] = corrent_lf['value']
                            corrent_result['uec'] = corrent_uec['value']
                            corrent_result['time'] = corrent_lf['col_time']
                    elif 0 < lf_index < len(self.pointLfs) - 1:  # 当纵做在2-9 之间
                        if corrent_lf['value'] is not None and corrent_lf['value'] != '-':
                            if self.pointLfs[lf_index - 1] <= float(corrent_lf['value']) < self.pointLfs[
                                lf_index]:  # 如果当天的负荷率大于前一个值 ，小于当前值
                                # 判断uec的返回
                                if len(uecRange) == 2:  # 如果uecRange是一个区间
                                    #print(type(corrent_uec['value']))
                                    #print(corrent_uec['value'])
                                    if uecRange[0] <= corrent_uec['value'] < uecRange[1]:  # 如果uec的值在最大值之间

                                        #statues = 0
                                        statusCode=1
                                    elif uecRange[1] <= corrent_uec['value']:  # 如果当前的值大于较大值，则异常：
                                        #statues = -1
                                        statusCode=0
                                    else:  # 如果当前值小于较小的值，则为良好
                                        #statues = 1
                                        statusCode=2
                                elif len(uecRange) == 1:  # 如果uecRange只有一个值
                                    if uecRange[0] <= corrent_uec['value']:  # 如果大于该值，正运行良好
                                        #statues = 0
                                        statusCode=1
                                    else:  # 否则运行良好
                                        #statues = 1
                                        statusCode=2
                                corrent_result['code'] = code
                                corrent_result['statusCode'] = statusCode
                                corrent_result['status'] = statues_code[statusCode]
                                corrent_result['lf'] = corrent_lf['value']
                                corrent_result['uec'] = corrent_uec['value']
                                corrent_result['time'] = corrent_lf['col_time']

                        else:
                            corrent_result['code'] = code
                            corrent_result['statusCode'] = -1
                            corrent_result['status'] = statues_code[-1]
                            corrent_result['lf'] = corrent_lf['value']
                            corrent_result['uec'] = corrent_uec['value']
                            corrent_result['time'] = corrent_lf['col_time']
                    elif lf_index == len(self.pointLfs) - 1:  # 如果是最后一个值
                        if corrent_lf['value'] is not None and corrent_lf['value'] != '-':
                            if self.pointLfs[lf_index - 1] <= float(corrent_lf['value']):  # 如果当天的负荷率大于前一个值 ，小于当前值
                                # 判断uec的返回
                                if len(uecRange) == 2:  # 如果uecRange是一个区间
                                    if uecRange[0] <= corrent_uec['value'] < uecRange[1]:  # 如果uec的值在最大值之间
                                        #statues = 0
                                        statusCode=1
                                    elif uecRange[1] <= corrent_uec['value']:  # 如果当前的值大于较大值：
                                        #statues = -1
                                        statusCode=0
                                    else:  # 如果当前值小于较小的值，则为良好
                                        #statues = 1
                                        statusCode=2
                                elif len(uecRange) == 1:  # 如果uecRange只有一个值
                                    if uecRange[0] <= corrent_uec['value']:  # 如果大于该值，正运行良好
                                        #statues = 0
                                        statusCode=1
                                    else:  # 否则运行良好
                                        #statues = 1
                                        statusCode=2
                                corrent_result['code'] = code
                                corrent_result['statusCode'] = statusCode
                                corrent_result['status'] = statues_code[statusCode]
                                corrent_result['lf'] = corrent_lf['value']
                                corrent_result['uec'] = corrent_uec['value']
                                corrent_result['time'] = corrent_lf['col_time']

                        else:
                            corrent_result['code'] = code
                            corrent_result['statusCode'] = -1
                            corrent_result['status'] = statues_code[-1]
                            corrent_result['lf'] = corrent_lf['value']
                            corrent_result['uec'] = corrent_uec['value']
                            corrent_result['time'] = corrent_lf['col_time']

                result_temp_list.append(corrent_result)
            result_list.append(result_temp_list)
        return result_list

    def EfficiencyAnyalysisDetails(self,payload): #散点图主函数

        if 'deviceIds' in payload.keys(): #设备散点图分析
            #首先判断传入时间，是否为班组，或者默认时间
            time_payload={'stationId':payload['stationId']}
            if 'isTeam' in payload.keys():# 如果参数中传入isTeam
                time_payload['isTeam']=payload['isTeam']
            if 'startTime' in payload.keys() and 'endTime' in payload.keys(): #如果参数中传入时间
                time_payload['startTime']=payload['startTime']
                time_payload['endTime'] = payload['endTime']
            time_zone=self.time_zone.getDateTime(time_payload)

            #获取系统测点
            result=[]
            for device_list in payload['deviceIds']:
                checkPoint=self.getDeviceCheckPoint(device_list['deviceId'])

                fact_data=self.requestDataService(payload['stationId'],checkPoint,time_zone) #事实数据
                SD_LIST=self.dispersePoint(fact_data)['data']#获取散点列表及散点个数
                #print(SD_LIST)
                SD_DICT={device_list['deviceId']:SD_LIST}
                analysis_result=self.analysis(SD_DICT,device_list['consumeMax']) #获得散点图数据，及负每个负荷率下最大的单耗概率
                result.append(analysis_result)
            #print(result)
            return result

        elif 'systems' in payload.keys():#系统散点图分析
            # 首先判断传入时间，是否为班组，或者默认时间
            time_payload = {'stationId': payload['stationId']}
            if 'isTeam' in payload.keys():  # 如果参数中传入isTeam
                time_payload['isTeam'] = payload['isTeam']
            if 'startTime' in payload.keys() and 'endTime' in payload.keys():  # 如果参数中传入时间
                time_payload['startTime'] = payload['startTime']
                time_payload['endTime'] = payload['endTime']
            time_zone = self.time_zone.getDateTime(time_payload)

            result=[]
            for system in payload['systems']:
                checkPoint = self.getSystemCheckPoint(system['sysId'],system['sysType'],payload['stationId'])

                fact_data = self.requestDataService(payload['stationId'], checkPoint, time_zone)  # 事实数据
                #print(fact_data)
                SD_LIST = self.dispersePoint(fact_data)['data']  # 获取散点列表及散点个数
                SD_DICT = {system['sysId']: SD_LIST}
                analysis_result = self.analysis(SD_DICT, system['consumeMax'])  # 获得散点图数据，及负每个负荷率下最大的单耗概率
                result.append(analysis_result)
            #print(result)
            return result


    def dispersePoint(self,args):  # 返回散点列表，第一个字段为LF，第二个字段为UEC或COP，如果同一时间点缺少其中任意数据则该点不在统计范围

        LF_list=list(filter(lambda x:x['code'].endswith('LF'),args))[0]['datas'] #负荷率散点
        uec_list=list(filter(lambda x:not x['code'].endswith('LF'),args))[0]['datas'] #能效或单耗散点
        sanDian_list=[]
        for LF_item in LF_list:
            if LF_item['value'] is not None and LF_item['value'] != '':
                sanDian = []
                sanDian.append(LF_item['value'])
                for UEC_item in uec_list:
                    if UEC_item['col_time']==LF_item['col_time'] and UEC_item['value'] is not None and UEC_item['value'] != '':
                        sanDian.append(UEC_item['value'])
                        break
                if len(sanDian) ==2:
                    if sanDian[0] !=0 or sanDian[1] !=0:
                        sanDian_list.append(sanDian)
        SD_NUM=len(sanDian_list)
        result={'lenth':SD_NUM,'data':sanDian_list}
        return result

    def analysis(self,param, consumeMax):  # 接收dispersePoint返回的数据,以及纵坐标数据,返回散点图结果数据
        pointLfs = self.pointLfs
        result = {}
        for tempValue in param:  # 每个设备
            SDLenth = len(param[tempValue])  # 获取点的个数
            SDlist = []
            #print(SDLenth)
            #print(param[tempValue])
            for consumeMaxIndex in range(0, len(consumeMax) ):  # 循环纵坐标
                TJList = []
                for pointLfsIndex in range(0, len(pointLfs)):  # 循环横坐标
                    index = 0
                    for value in param[tempValue]:#获取每个散点

                        if 0 <= consumeMaxIndex < len(consumeMax)-1: #纵坐标取0-last-1
                            if consumeMax[consumeMaxIndex ] <= value[1] < consumeMax[consumeMaxIndex+1]:
                                if pointLfsIndex == 0: #如果横坐标是第一个值
                                    if value[0] <= pointLfs[pointLfsIndex]: #取所有小于第一值的数据
                                        index += 1
                                elif 0 < pointLfsIndex <= len(pointLfs)-2: #如果横坐标是2到len-1个值 第九个值，index 为8
                                    if pointLfs[pointLfsIndex - 1] <= value[0] < pointLfs[pointLfsIndex]:#取当前坐标与前一坐标之间的值
                                        index += 1
                                elif pointLfsIndex==len(pointLfs)-1: #横坐标为最后一个值，取大于倒数第二值的所有值
                                    if pointLfs[pointLfsIndex - 1] <= value[0]:
                                        index += 1
                        elif consumeMaxIndex==len(consumeMax)-1: #横坐标取最后一个值
                            if value[1] >= consumeMax[consumeMaxIndex]: #横坐标去大于最后一个值的所有数据
                                if pointLfsIndex == 0: #如果横坐标是第一个值
                                    if value[0] <= pointLfs[pointLfsIndex]: #取所有小于第一值的数据
                                        index += 1
                                elif 0 < pointLfsIndex <= len(pointLfs)-2: #如果横坐标是2到len-1个值 第九个值，index 为8
                                    if pointLfs[pointLfsIndex - 1] <= value[0] < pointLfs[pointLfsIndex]:#取当前坐标与前一坐标之间的值
                                        index += 1
                                elif pointLfsIndex==len(pointLfs)-1: #横坐标为最后一个值，取大于倒数第二值的所有值
                                    if pointLfs[pointLfsIndex - 1] <= value[0]:
                                        index += 1

                    TJList.append(index)
                if SDLenth > 0:
                    #print (TJList)
                    tempList = list(map(lambda x: x / SDLenth * 100, TJList))
                    tempList1 = list(map(lambda x: '-' if x == 0 else floatFormat(x, 3), tempList))

                else:
                    print('散点个数为0')
                    continue
                SDlist.append(tempList1)
            pointCounts = list(reversed(SDlist))  #散点图


            lf_MaxRato=[] #接收以负荷率为准的概率图
            for index_list in range(0,len(pointLfs)):  #获取每个负荷率中比重最大的单耗概率
                temp=[]
                for index in range(0,len(pointCounts)):#
                    temp.append( pointCounts[index][index_list])
                lf_MaxRato.append(list(reversed(temp)))
            #print(lf_MaxRato)
            pointMaxCounts=[] #同一负荷率下，最大的单耗所占的比重。
            for item in lf_MaxRato:
                #print(item)
                pointMaxCounts.append(self.getMaxValueInList(item))
            #获取负荷率对应的单耗最大值
            pointMaxWithLF_value=[]
            for item in lf_MaxRato:
                maxValueRange=[]
                maxIndex=self.getMaxValueInDict(item)
                #print(maxIndex)
                if maxIndex<len(consumeMax)-1:#不是最后一个坐标
                    maxValueRange.append(consumeMax[maxIndex])
                    maxValueRange.append(consumeMax[maxIndex+1])
                else:
                    maxValueRange.append(consumeMax[maxIndex])
                pointMaxWithLF_value.append(maxValueRange)
            #print(pointMaxWithLF_value)
            resultTemp={}
            resultTemp['pointMaxCounts']=pointMaxCounts
            resultTemp['pointCounts'] = pointCounts
            resultTemp['pointMaxWithLF_value']=pointMaxWithLF_value
            result[tempValue]=resultTemp

        #print(result)
        return result

    def format_change(self,timeList, vlaueList):
        copValueList = copy.deepcopy(timeList)
        copTimeList = copy.deepcopy(timeList)
        index = []
        for item in vlaueList:
            if item['date'] in copValueList:
                index1 = copValueList.index(item['date'])
                copValueList[index1] = item['value']
                index.append(index1)
        ii = []
        for i in range(0, len(copValueList)):
            ii.append(i)
        notin = []
        for i in ii:
            if i not in index:
                notin.append(i)
        for index in notin:
            copValueList[index] = ''

        result = {'timeList': copTimeList, 'valueList': copValueList}
        return result


    def getDeviceCheckPoint(self,deviceId):
        if deviceId.find('ECR')+1 or deviceId.find('HP')+1:  # 如果是热泵或者电制冷机，返回cop和lf

            uecCode=deviceId+'_COP'
            lfCode=deviceId+'_LF'
        else:
            uecCode = deviceId + '_UEC'
            lfCode = deviceId + '_LF'
        return uecCode+','+lfCode

    def getSystemCheckPoint(self,sysID,sysType,stationId): #获取系统的测点

        uecCode=''
        lfCode=''
        if sysType in ['ECR','HP']:  # 如果是热泵或者电制冷机，返回cop和lf
            uecCode=stationId+'_'+sysType+'_COP'
            lfCode=stationId+'_'+sysType+'_LF'
        elif sysType=='CCHP':
            payload={ "containerId": stationId,"sysId": sysID}
            #print(payload)
            self.cim.post_cim_by_containerId_sysId(payload)
            devices =self.cim.rest.json_result()['deviceList']
            ICG_list=list(filter(lambda x:x['deviceType']=='ICG',devices))
            ICG_ID=list(map(lambda x:x['deviceId'],ICG_list))[0] #业务上说，一套cchp只有一个ICG
            uecCode = ICG_ID + '_UEC'
            lfCode = ICG_ID + '_LF'
        else:
            uecCode = stationId+'_'+sysType+ '_UEC'
            lfCode = stationId+'_'+sysType+ '_LF'
        return uecCode+','+lfCode
    def requestDataService(self,stationId,checkPoint,time_zone): #请求服务返回设备的数据
        payload={"token": "asdfasd", "projectId": stationId, "type": "HH", "codes": checkPoint,
         "endDate": time_zone['endTime'], "beginDate": time_zone['startTime'], "downsample": "30m"}
        self.data_service_interface.post_ds_getldata(payload)
        return self.data_service_interface.rest.json_result()['data']

    def getMaxValueInList(self,listParam): #获取列表中的最大值
        templist=[] #存放数字
        for item in listParam:
            if not item.find('-')+1:#如果只包含字符串
                templist.append(float(floatFormat(item,3)))
        if templist: #如果tempList不为空，则比较其中最大的值
            maxValue=max(templist)
        else:
            maxValue=0
        return maxValue

    def getMaxValueInDict(self,listParam): #返回最大值对应纵坐标的序号
        maxIndex = 0  # 最大值默认为0
        tempDict = {}  # 存放数字
        for index in range(0, len(listParam)):
            if not listParam[index].find('-') + 1:  # 如果只包含字符串
                tempDict[index] = float(floatFormat(listParam[index], 3))
        # print(tempDict)
        if tempDict:  # 如果tempList不为空，则比较其中最大的值
            maxIndex = max(tempDict, key=tempDict.get)
        else:
            maxIndex = 0
        #print(maxIndex)
        return maxIndex
class TimeZone():
    def __init__(self,):
        self.os_ues = eval(ReadCfgFile().get_val('database', 'os_ues'))

    def getDateTime(self,payload):#返回统计时间   payload={"isTeam":1,"stationId":"CA01ES01","startTime":"","endTime": "",}  #如果处在isTeam且为1，则取班组时间。如果startTime和endTime存在且值不为空，则取设置好的值。如果isTeam，startTime，endTime均无效，则取过去一年到当前的时间

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
            firstStage=teamTimeZone[0]
            secondStage = teamTimeZone[1]
            #调整阶梯的顺序，将在一天内连续时间段的设置为第一阶梯，跨天的设置为第二阶梯
            if int(firstStage['start'].split(':')[0])<int(firstStage['end'].split(':')[0]):
                pass
            else:
                tempStage=firstStage
                firstStage=secondStage
                secondStage=tempStage
            if int(firstStage['start'].split(':')[0])<=nowHour<int(firstStage['end'].split(':')[0]): #如果当前时间的小时在第一阶梯之间
                teamTimeStage['startTime']=(datetime.now().replace(hour=int(firstStage['start'].split(':')[0]),minute=int(firstStage['start'].split(':')[1]),second=0)).strftime('%Y-%m-%d %H:%M:%S')
                teamTimeStage['endTime'] = (datetime.now().replace(hour=int(firstStage['end'].split(':')[0]),minute=int(firstStage['end'].split(':')[1]),second=0)).strftime('%Y-%m-%d %H:%M:%S')
            else:#当前时间的小时不在第一阶梯则取第二阶梯

                teamTimeStage=self.judgeTeamTime(secondStage,nowHour)
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

    def getTeamTime24H(self,stationId): #根据当前时间返回一天的班组时间
        teamTimeRange = {}
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
            firstStage = teamTimeZone[0]
            secondStage = teamTimeZone[1]
            # 调整阶梯的顺序，将在一天内连续时间段的设置为第一阶梯，跨天的设置为第二阶梯
            if int(firstStage['start'].split(':')[0]) < int(firstStage['end'].split(':')[0]):
                pass
            else:
                tempStage = firstStage
                firstStage = secondStage
                secondStage = tempStage
            teamTimeRange=self.judgeTeamTime24H(firstStage,nowHour)
        return  teamTimeRange

    def judgeTeamTime24H(self,firstStage,nowHour): #根据当前时间返回24小时区间
        teamTimeStage={}
        if int(firstStage['start'].split(':')[0])<=nowHour: #第一阶梯的开始时间小于当前时间
            teamTimeStage['startTime']=(datetime.now().replace(hour=int(firstStage['start'].split(':')[0]),minute=int(firstStage['start'].split(':')[1]),second=0)).strftime('%Y-%m-%d %H:%M:%S')
            teamTimeStage['endTime'] = ((datetime.now()+timedelta(days=1)).replace(hour=int(firstStage['start'].split(':')[0])-1, minute=int(firstStage['start'].split(':')[1]),second=0)).strftime('%Y-%m-%d %H:%M:%S')
        elif 0<=nowHour<int(firstStage['start'].split(':')[0]):#当前时间为0点以后，且小于第一阶梯的开始时间

            teamTimeStage['startTime'] = ((datetime.now()-timedelta(days=1)).replace(hour=int(firstStage['start'].split(':')[0]), minute=int(firstStage['start'].split(':')[1]),second=0)).strftime('%Y-%m-%d %H:%M:%S')
            teamTimeStage['endTime'] = (datetime.now() .replace(hour=int(firstStage['start'].split(':')[0])-1, minute=int(firstStage['start'].split(':')[1]),second=0)).strftime('%Y-%m-%d %H:%M:%S')
        else:
            print('班组时间第二阶段设置错误')
        return teamTimeStage


if __name__=='__main__':
    Eff=EfficiencyAnyalysisDetails()
    # payload={  "deviceIds":[{"deviceId":"GSB_GSB01","consumeAverage":0.2,"consumeMax":[0,30,60,90,110]}],
    #                         "isTeam":0,
    #                         "stationId":"CA30ES03",
    #                         #"startTime":"2018-07-16 00:00:00",#2018-07-16 00:00:00
    #                         #"endTime": "2018-07-16 23:59:59",#2018-07-16 23:59:59
    #                         }
    # Time_payload={"isTeam":1,"stationId":"CA01ES01","startTime":"2016-08-18 14:29:28","endTime": "2018-08-18 14:29:28",}

    # payload={
    #     "systems": [{"sysId": "CA01ES01_CCHP01", "sysName": "longyou", "sysType": "CCHP", "consumeAverage": 0.2,
    #                  "consumeMax": [0.0, 30.0, 60.0, 90.0, 110.0]}],
    #     "startTime": "2018-06-01 00:00:00",
    #     "endTime": "2018-06-30 23:00:00",
    #     "stationId": "CA01ES01"
    # }
#     payload={
#     "systems":[{"sysId":"CA30ES03_GSB01","sysName":"longyou","sysType":"GSB","consumeAverage":0.2,"consumeMax":[0.0,30.0,60.0,90.0,110.0]}],
#     #"startTime":"2018-08-01 00:00:00",
#     #"endTime":"2018-08-30 23:00:00",
#     "stationId":"CA30ES03"
# }
#     TimeZone1=TimeZone()
#     print(TimeZone1.getDateTime(Time_payload))

    #payload={"deviceIds":[{"deviceId":"ICG_ICG01","consumeAverage":0.2,"consumeMax":[0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4],"deviceName":"1#燃气内燃机发电机组","deviceType":"ICG"}],"endTime":"2018-08-23 23:59:59","isTeam":0,"sortByTime":"","startTime":"2018-08-21 00:00:00","stationId":"CA01ES01","sysId":"CA01ES01_CCHP02","timeScale":"HH"}
    #payload={"systems":[{"sysId":"CA01ES01_GSB01","sysName":"燃气蒸汽锅炉单元","sysType":"GSB","consumeAverage":0.2,"consumeMax":[0,40,60,70,75,80,85,90,100,120]}],"startTime":"2018-08-23 00:00:00","endTime":"2018-08-23 23:59:00","stationId":"CA01ES01","isTeam":1}
    payload={"deviceIds":[{"deviceId":"GSB_GSB01","consumeAverage":0.2,"consumeMax":[0,40,60,70,75,80,85,90,100,120],"deviceName":"1#燃气蒸汽锅炉"}],"stationId":"CA01ES01","sort":"2","type":"HH"}
    #Eff.EfficiencyAnyalysisDetails(payload)
    #payload={"deviceIds":[{"deviceId":"GSB_GSB01","consumeAverage":0.2,"consumeMax":[0,40,60,70,75,80,85,90,100,120],"deviceName":"1#燃气蒸汽锅炉"},{"deviceId":"GSB_GSB02","consumeAverage":0.2,"consumeMax":[0,40,60,70,75,80,85,90,100,120],"deviceName":"2#燃气蒸汽锅炉"},{"deviceId":"GSB_GSB03","consumeAverage":0.2,"consumeMax":[0,40,60,70,75,80,85,90,100,120],"deviceName":"3#燃气蒸汽锅炉"}],"isTeam":1,"stationId":"CA02ES01"}
    #Eff.currentPoints(payload)
    #payload={"deviceIds":[{"deviceId":"GSB_GSB01","consumeAverage":0.2,"consumeMax":[0,40,60,70,75,80,85,90,100,120],"deviceName":"1#燃气蒸汽锅炉"}],"isTeam":1,"stationId":"CA02ES01"}
    #payload={"deviceIds":[{"deviceId":"GSB_GSB01","consumeAverage":0.2,"consumeMax":[0,40,60,70,75,80,85,90,100,120],"deviceName":"1#燃气蒸汽锅炉"},{"deviceId":"GSB_GSB02","consumeAverage":0.2,"consumeMax":[0,40,60,70,75,80,85,90,100,120],"deviceName":"2#燃气蒸汽锅炉"},{"deviceId":"GSB_GSB03","consumeAverage":0.2,"consumeMax":[0,40,60,70,75,80,85,90,100,120],"deviceName":"3#燃气蒸汽锅炉"}],"isTeam":1,"stationId":"CA02ES01"}
    #payload={"systems":[{"sysId":"CA02ES01_GSB01","consumeAverage":0.2,"sysType":"GSB","consumeMax":[0,40,60,70,75,80,85,90,100,120],"sysName":"燃气蒸汽锅炉单元"}],"stationId":"CA02ES01","isTeam":"1"}
    #payload={"systems":[{"sysId":"CA01ES01_CCHP01","consumeAverage":0.2,"sysType":"CCHP","consumeMax":[0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4],"sysName":"1#CHP单元"},{"sysId":"CA01ES01_CCHP02","consumeAverage":0.2,"sysType":"CCHP","consumeMax":[0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4],"sysName":"2#CHP单元"},{"sysId":"CA01ES01_GSB01","consumeAverage":0.2,"sysType":"GSB","consumeMax":[0,40,60,70,75,80,85,90,100,120],"sysName":"燃气蒸汽锅炉单元"}],"stationId":"CA01ES01","isTeam":1}
    #payload={"deviceIds":[{"deviceId":"ICG_ICG01","consumeAverage":0.2,"consumeMax":[0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4],"deviceName":"1#燃气内燃机发电机组"}],"isTeam":1,"stationId":"CA01ES01"}
    #payload={"stationId":"CA01ES01","deviceIds":[{"deviceId":"ICG_ICG01","consumeAverage":0.2,"consumeMax":[0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4],"deviceName":"1#燃气内燃机发电机组"}]}
    #payload={"stationId":"CA02ES01","deviceIds":[{"deviceId":"GTG_GTG01","consumeAverage":0.2,"consumeMax":[0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4],"deviceName":"燃气轮机发电机组"}]}
    #Eff.analysisCalendars(payload)
    #Eff.copGoodInMonth(payload)
    Eff.getMaxProbability(payload)
