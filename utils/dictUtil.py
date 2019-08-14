# __*__coding=utf-8__*__
# autor 张鹏
# date 2018/05/23
# describe  字典处理工具

import unittest

#
# def compareKey(self,dict1,dict2):  #获取字典中的key,两个字典中的key值相同。
#     dict1_key_list =dict1.keys() #获取第一个字典所有key
#     for key in dict2.iterkeys():
#         if key in dict1_key_list:
#             self.assertEqual(dict1[key],dict2[key],'%s比对不同过' %(key))
#         else:
#             print ('两处结果集，字段不相同'+key)
#
#
# def test1(obj, list1, list2,primaryKey):#本函数用于比对两个字典列表,形如[{},{}]，
#     flag =True
#     if len(list1)==len(list2) & len(list1)==0:
#         for temp1 in list1:
#             if isinstance(temp1,dict): #判断内部类型为字典 如果为字典，则执行下面的语句
#                 for temp2 in list2:
#                     if isinstance(temp2, dict):#判断内部类型为字典
#                         if temp1[primaryKey] == temp2[primaryKey]:  # 如果主键的值相同，则说明为同一条数据。
#                             temp_key_list = temp2.keys()
#                             for key in temp_key_list:
#                                 obj.assertEqual(str(temp1[key]), str(temp2[key]),msg='primaryKey为{primaryKey}，字段为{key}的值不相等'.format(primaryKey=primaryKey,key=key))
#             elif
#     else:
#         flag=False
#         obj.assertTrue(flag,msg='传入两个列表的长度不同或为空')
class test(unittest.TestCase):

    def test(self):
        list1=[{'abnoPhenId': 'JSB_DLBX', 'alarmContent': '给水泵电流变小', 'alarmId': 100464, 'alarmLevel': 1402,
          'alarmLevelName': '1级', 'alarmSource': 1501, 'alarmSourceName': '运维大脑', 'alarmStatus': 1102,
          'alarmStatusName': '未解决', 'alarmType': 1802, 'alarmTypeName': '能效异常', 'createTime': '2018-04-10 17:26:13'},
         ]

        list2=[{ 'alarmContent': '给水泵电流变小','abnoPhenId': 'JSB_DLBX',  'alarmLevel': 1402,'alarmId': 100464,
          'alarmLevelName': '1级', 'alarmSource': 1501, 'alarmSourceName': '运维大脑', 'alarmStatus': 1102,
          'alarmStatusName': '未解决', 'alarmType': 1802, 'alarmTypeName': '能效异常', 'createTime': '2018-04-10 17:26:13'},
        ]



        compare(self,list1,list2)


def compare(obj,para1,para2,primaryKye=None): #
    flag =True
    if isinstance(para1,dict) & isinstance(para2,dict):  #先判断两个传入值是否为字典
        #先判断两个字典的key是否相同
        obj.assertDictEqual(para1,para2)


    elif isinstance(para1,list) & isinstance(para2,list): #判断两个传入值是否为列表
        obj.assertListEqual(para1,para2)
    else:
        flag=False
        obj.assertTrue(flag,msg='两种数据类型不相同，或不是字典与列表类型，无法比较')

if __name__=='__main__':
    unittest.main()