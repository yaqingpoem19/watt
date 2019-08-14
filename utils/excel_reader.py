#__*__utf-8__*__

#autor zhangpeng
#2018-05-18
#excel工具类，用于读取Excel中的数据
#
##########

import xlrd
from utils.read_config import ReadCfgFile
import  sys
import  datetime
from xlrd import xldate_as_tuple


#Excel 处理工具类
class excelUtil(object):

    def __init__(self,sheetIndex=0,sheetName='Sheet1'): #默认获取第一个sheet,默认sheetname为Sheet1
        self.path=ReadCfgFile().get_val('global', 'excel_path')  #初始化Excel路径
        self.sheetIndex=sheetIndex
        self.sheetName=sheetName


    def read_excel_list(self): #返回一个二维列表

        sheetRows=0
        sheetCols=0
        '''Read Excel with xlrd'''
        # file
        TC_workbook = xlrd.open_workbook(self.path)

        # 获取所有sheet名称
        all_sheets_list = TC_workbook.sheet_names()
        print("All sheets name in File:", all_sheets_list)


        second_sheet = TC_workbook.sheet_by_name(self.sheetName)
        sheetRows=second_sheet.nrows
        sheetCols=second_sheet.ncols

        print(u'共有 %d 条用例' %sheetRows)
        list=[]
        if sheetRows>0 :
            for item in range(sheetRows):
                list.append(second_sheet.row_values(item))
        else :
            print (u"没有可执行的用例！")

        return list

    def read_excel_dict(self): #返回字典列表，首行做为key


        TC_workbook = xlrd.open_workbook(self.path)
        sheet=TC_workbook.sheet_by_name(self.sheetName)
        sheetRows = sheet.nrows
        sheetCols = sheet.ncols
        list = []
        if sheetRows ==0 :
            print (u"Excel中没有数据，请确认路径是否正常！")
            sys.exit()
        else:

            firstRow_temp= sheet.row_values(rowx=0, start_colx=0, end_colx=sheetCols) #获取首行值作为字典的key
            for item_row in range(1,sheetRows):
                dict_temp={}
                for item_col in range(0,sheetCols):
                    ctype=sheet.cell(item_row,item_col).ctype
                    cell_temp=sheet.cell_value(item_row,item_col)
                    if ctype==2 and cell_temp % 1 ==0 : #整型
                        cell_temp=int(cell_temp)
                    elif ctype==3:
                        date = datetime(*xldate_as_tuple(cell_temp, 0))
                        cell = date.strftime('%Y/%d/%m %H:%M:%S')
                    elif ctype == 4:
                        cell = True if cell_temp == 1 else False
                    dict_temp[firstRow_temp[item_col]]=cell_temp
                list.append(dict_temp)

        return list




if __name__ == "__main__":
    excelUtil1 = excelUtil(sheetName='Sheet1')
    excelUtil1.read_excel_dict()




