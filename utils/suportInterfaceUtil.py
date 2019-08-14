# __*__coding=utf-8__*__
# autor 张鹏
# date  2018/07/17
# describe 支持测试接口类

import requests

class PyREST(object):
    def __init__(self, endpoint, header={'Content-Type': 'application/json', 'Connection': 'close'}):
        self.session = requests.session()
        self.session.headers.update(header)
        self.response = requests.Response()
        self.endpoint = endpoint

    def get(self, resource, params=None, stream=False):
        self.response = self.session.get(self.endpoint+resource, params=params, stream=stream)
        return self.response

    def post(self, resource, payload=None, params=None):
        self.response = self.session.post(self.endpoint+resource, json=payload, params=params)
        return self.response

    def post_data(self,resource,data=None):
        #header = {'Content-type': 'application/x-www-form-urlencoded', 'Connection': 'keep-alive'}
        #self.session.headers.update(header)

        self.response = self.session.post(self.endpoint + resource,data)
        print(self.response.url)
        return self.response

    def post_file(self, resource, files):
        self.response = self.session.post(self.endpoint+resource, files=files)

    def put(self, resource, payload=None, params=None):
        self.response = self.session.put(self.endpoint+resource, json=payload, params=params)

    def option(self, resource):
        self.response = self.session.options(self.endpoint+resource)
        return self.response

    def delete(self, resource):
        self.response = self.session.delete(self.endpoint+resource)
        return self.response

    def url(self):
        return self.response.url

    def json_result(self):
        '''
            response result returned as a json format.
        '''
        return self.response.json()

    def text(self):
        '''
            response result returned as a txt format.
        '''
        return self.response.text

class cim_api():

    def __init__(self, header={'Content-Type': 'application/json', 'Connection': 'keep-alive'}):
        self.endpoint='http://cim-fnw-test.topaas.enncloud.cn'
        self.rest = PyREST(self.endpoint, header)
    #获取指定站下所有系统
    def  post_sys_by_containerId(self,payload):
        resource='/cim/business/query/sys/by/containerId'
        self.rest.post(resource,payload)
    #获取站下指定系统的设备
    def post_cim_by_containerId_sysId(self,payload):
        resource='/cim/business/query/sys/by/containerId/and/sysId'
        self.rest.post(resource, payload)


class user_cim_api():
    def __init__(self, endpoint, header={'Content-Type': 'application/json', 'Connection': 'keep-alive'}):
        self.rest = PyREST(endpoint, header)

        #	根据stationId获取关联企业列表
    def post_station_getEnterpriseByStationId(self,payload=None,params=None):
        resource ='/station/getEnterpriseByStationId'
        self.rest.post(resource, payload=payload,params=params)

    #根据企业Openid以及能源类型获取企业所关联的量测点
    def post_metric_getEnterpriseMetricByOpenidAndEnergyType(self,payload):
        resource = '/metric/getEnterpriseMetricByOpenidAndEnergyType'
        self.rest.post(resource, payload)

    def post_station_getEnterpriseTypeByStationId(self,payload=None,params=None): #根据stationId获取关联企业列表(按照企业行业区分)
        resource = '/station/getEnterpriseTypeByStationId'
        self.rest.post(resource, payload=payload, params=params)


class dataService_interface():
    def __init__(self, endpoint, header={'Content-Type': 'application/json', 'Connection': 'keep-alive'}):
        self.rest = PyREST(endpoint, header)
    #获取时间范围时间求和值
    def post_ds_getsumdata(self,payload):
        resource ='/ds/getsumdata'
        self.rest.post(resource, payload)
    #	获取曲线数据
    def post_ds_getldata(self,payload):
        resource = '/ds/getldata'
        self.rest.post(resource, payload)

    def post_ds_getsumdatagrouptime(self,payload): #获取时间范围CODE求和值
        resource ='/ds/getsumdatagrouptime'
        self.rest.post(resource, payload)

