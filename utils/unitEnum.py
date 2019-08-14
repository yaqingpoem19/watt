# __*__coding=utf-8__*__
# autor 张鹏
# date 2018/09/11
# describe 单位枚举类


from enum import Enum


class Unit(Enum):
    UNIT_COP="%" # 能效
    UNIT_EETA="%"# 综合能效
    UNIT_G_UEC="Nm³/kWh" # 热水锅炉单耗GWB CCHP单耗
    UNIT_GWB_UEC="Nm³/t" # 蒸汽锅炉单耗GSB
    UNIT_LF="%" # 负荷率
    UNIT_NULL=""# 无单位
if __name__=='__main__':
    print(Unit.UNIT_COP.value)