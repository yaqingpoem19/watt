                                            watt简介


一. watt是什么
    watt是一个基于python语言开发的自动化测试框架。目前，watt支持REST API的接口测试，后续watt会持续扩展支持web UI和移动端的自动化测试。

二. watt的组成
    watt由pyrest,runner,runningplan,testscripts和utils组成。各模块功能如下：
    1.pyrest：对requests进行封装实现常用的http请求（pyrest.py）以及基于被测业务封装的api（api.py）
    2.testscripts: 所有的自动化测试脚本存放于此
    3.utils: 写自动化脚本时所需的一些工具类
    4.runner：驱动自动化脚本运行
    5.runningplan：根据不同的测试需求选择自动化脚本的运行方式

三. watt使用环境安装
    1.安装python3
    2.安装virtualenv
    3.从 https://source.enncloud.cn/ 获取watt
    4.在watt项目内启用virtualenv
    5.在virtual env中使用"pip install -r requirements.txt"安装watt所需类库

四. 如何使用watt做接口测试
    1.根据被测业务接口，在api.py中对其进行封装。
    2.在testscripts下根据接口测试用例使用步骤1中封装的接口完成接口自动化测试脚本
        1) 脚本名称必须以test_开头
        2）测试类中的测试方法必须以test_开头
        3）测试脚本示例请参考test_demo.py
    3.在runnuningplan中可以选择如下两种运行方式
        1）运行指定路径下的全部脚本, 使用run_all_tests.py, 测试脚本路径在cfg.ini中的test_path定义。
        2）运行指定路径下的指定脚本, 使用run_smoke_tests.py, 测试脚本路径在cfg.ini中的est_path定义（不常用，初次使用可不关注此模式）。
    4.测试脚本支持参数化，相应脚本的参数化内容放置在指定运行方式（runningplan）下的cfg.ini中，使用ReadCfgFile类读取参数化内容。

五.  脚本运行结果展示
    1.第一次使用runningplan下的运行方式运行脚本时会自动创建一个report目录，所有使用该种运行方式的测试结果都会保存在该目录下。
    2.测试结果格式为html文档，文件名使用测试时间标识。
    3.测试结果分为pass，fail和error三种，使用浏览器打开测试结果文档后可查看本次所有运行脚本的运行结果。