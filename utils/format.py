# __*__coding=utf-8__*__
# autor 张鹏
# date 2018/7/10
# describe 添加float格式转换函数
import sys
import calendar
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
def floatFormat(value,definition=2):
    if isinstance(value,float):#如果是float
        #首先转换成字符串

        value=str(value)
        sign=''
        if value.startswith('-'):
            value =value[1:]
            sign='-'
        temp=value.split('.')
        valueDict={'Inter':list(map(lambda x:int(x),temp[0])),'Decimal':list(map(lambda x:int(x),temp[1]))}
        decimalLen=len(valueDict['Decimal'])


        if decimalLen<definition: #原有小数位数小于期望的位数，则给后面的位数补0
            for item in range(0,definition-decimalLen):
                valueDict['Decimal'].append(0)
            inter = ''.join(list(map(lambda x: str(x), valueDict['Inter'])))
            decimal = ''.join(list(map(lambda x: str(x), valueDict['Decimal'])))

            exceptResult = sign+inter + '.' + decimal

            return exceptResult
        elif decimalLen==definition: #原有小数位数与期望位数相等，不做处理
            inter = ''.join(list(map(lambda x: str(x), valueDict['Inter'])))
            decimal = ''.join(list(map(lambda x: str(x), valueDict['Decimal'])))

            exceptResult = sign+inter + '.' + decimal

            return exceptResult
        else:#原有小数位数大于期望小数位数
            if valueDict['Decimal'][definition]<5: #如果近似位数的下一位小于5，直接舍去
                valueDict['Decimal']=valueDict['Decimal'][0:definition]
            elif valueDict['Decimal'][definition]>=5:#如果近似位数的下一位大于等于5，进1.
                valueDict['Decimal'][definition-1]+=1
                valueDict['Decimal'] = valueDict['Decimal'][0:definition]
                carry(valueDict['Inter'], valueDict['Decimal'], definition - 1)


        inter=''.join(list(map(lambda x: str(x), valueDict['Inter'])))
        decimal=''.join(list(map(lambda x: str(x), valueDict['Decimal'])))

        exceptResult=sign+inter+'.'+decimal

        return exceptResult
    elif isinstance(value,int):#如果是整型,则不存在进位的问题，只需要对给后面补上相应个数的0
        value=str(value)
        sign=''
        if value.startswith('-'):
            value=value[1:]
            sign='-'
        decimal='0'*definition
        exceptResult=sign+value+'.'+decimal

        return exceptResult
    elif isinstance(value,str):
        sign=''
        if value.startswith('-'):
            value=value[1:]
            sign='-'
        if value.find('.'):
            temp = value.split('.')
            valueDict = {'Inter': list(map(lambda x: int(x), temp[0])), 'Decimal': list(map(lambda x: int(x), temp[1]))}
            decimalLen = len(valueDict['Decimal'])


            if decimalLen < definition:  # 原有小数位数小于期望的位数，则给后面的位数补0
                for item in range(0, definition - decimalLen):
                    valueDict['Decimal'].append(0)
                inter = ''.join(list(map(lambda x: str(x), valueDict['Inter'])))
                decimal = ''.join(list(map(lambda x: str(x), valueDict['Decimal'])))

                exceptResult = sign+inter + '.' + decimal

                return exceptResult
            elif decimalLen == definition:  # 原有小数位数与期望位数相等，不做处理
                inter = ''.join(list(map(lambda x: str(x), valueDict['Inter'])))
                decimal = ''.join(list(map(lambda x: str(x), valueDict['Decimal'])))

                exceptResult = sign+inter + '.' + decimal

                return exceptResult
            else:  # 原有小数位数大于期望小数位数
                if valueDict['Decimal'][definition] < 5:  # 如果近似位数的下一位小于5，直接舍去
                    valueDict['Decimal'] = valueDict['Decimal'][0:definition]
                elif valueDict['Decimal'][definition] >= 5:  # 如果近似位数的下一位大于等于5，进1.
                    valueDict['Decimal'][definition - 1] += 1
                    valueDict['Decimal'] = valueDict['Decimal'][0:definition]
                    carry(valueDict['Inter'], valueDict['Decimal'], definition - 1)

            inter = ''.join(list(map(lambda x: str(x), valueDict['Inter'])))
            decimal = ''.join(list(map(lambda x: str(x), valueDict['Decimal'])))

            exceptResult =sign+ inter + '.' + decimal

            return exceptResult
        else:
            value=int(value)
            exceptResult=floatFormat(value,definition)
            return exceptResult
    else:
        print('无法处理的类型')
        sys.exit()

def carry(listInter,listDecimal,index):
    if listDecimal[index]==10 and index !=0:#如果小数list中index位==10 并且不是小数的第一位：
        listDecimal[index]=0
        listDecimal[index-1] +=1
        carry(listInter, listDecimal, index - 1)
    elif listDecimal[index]==10 and index ==0:#如果小数list中第一位==10 并且是小数的第一位：
        listDecimal[index] = 0
        listInter[-1]+=1
        carryInter(listInter,len(listInter)-1)


def carryInter(listInter,index):
    if listInter[index]==10 and index !=0 :#如果整数list中index的值为10 ，并且不是第一位
        listInter[index] = 0
        listInter[index - 1] += 1
        carryInter(listInter, index - 1)
    elif listInter[index]==10 and index ==0 :#如果整数list中，第一位元素为10
        listInter[index]=10


def thousandsChange(num,len=3):  #len为千分位长度

    if isinstance(num,float) or isinstance( num ,int):
        try:
            option=''
            value=str(num)
            if value.startswith('-'): #负数
                option='-'
                value=value[1:]
                value=value.split('.')
                if value.__len__()==2:
                    inter=list(map(lambda x :x,value[0]))
                    Decimal=list(map(lambda x :x,value[1]))
                    result=[]
                    index = 0
                    for item in reversed(inter):
                        if index <=len-1:
                            result.append(item)
                            index+=1
                        else:

                            result.append(',')
                            result.append(item)
                            index=1
                    result=list(reversed(result))
                    exceptResult=option+''.join(result)+'.'+''.join(Decimal)
                    print(exceptResult)
                    return exceptResult
                else:
                    inter = list(map(lambda x: x, value[0]))
                    result = []
                    index = 0
                    for item in reversed(inter):
                        if index <= len - 1:
                            result.append(item)
                            index += 1
                        else:

                            result.append(',')
                            result.append(item)
                            index = 1
                    result = list(reversed(result))
                    exceptResult=option+''.join(result)
                    print(exceptResult)
                    return exceptResult
            else:#正数
                value = value.split('.')
                if value.__len__() == 2:
                    inter = list(map(lambda x: x, value[0]))
                    Decimal = list(map(lambda x: x, value[1]))
                    result = []
                    index = 0
                    for item in reversed(inter):
                        if index <= len - 1:
                            result.append(item)
                            index += 1
                        else:

                            result.append(',')
                            result.append(item)
                            index = 1
                    result = list(reversed(result))
                    exceptResult = option + ''.join(result) + '.' + ''.join(Decimal)
                    print(exceptResult)
                    return exceptResult
                else:
                    inter = list(map(lambda x: x, value[0]))
                    result = []
                    index = 0
                    for item in reversed(inter):
                        if index <= len - 1:
                            result.append(item)
                            index += 1
                        else:

                            result.append(',')
                            result.append(item)
                            index = 1
                    result = list(reversed(result))
                    exceptResult = option + ''.join(result)
                    print(exceptResult)
                    return exceptResult
        except Exception as e:
            print('转换成字符串时出错：%s,%s' %(e.args[0],e.args[1]))




if __name__ == "__main__":
    # excelUtil1 = excelUtil(sheetName='Sheet1')
    # excelUtil1.read_excel_dict()
    a=-99
    place=5
    # print(floatFormat(a,place))
    # print(thousandsChange(50000.001,4))
    # print(datetime.now().strftime('%Y-%m-%d'))
    NOW=datetime.now()
    firstDayThreeMonthAgo = (datetime.now()-relativedelta(months=+3)).strftime('%Y-%m-01') #3个月前的第一天
    firstDay = datetime(NOW.year, NOW.month, 1, 23, 59, 59)
    upLast = (firstDay - timedelta(days=1)).strftime('%Y-%m-%d')  #上一月最后一天
    print(upLast)
    print(firstDayThreeMonthAgo)