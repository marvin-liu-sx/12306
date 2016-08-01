#! /usr/bin/env python3

'''
Train tickets query via command-line

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h, --help  显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 南京 北京 2016-07-01
'''


import os, re, sys, json
import requests
from requests.exceptions import ConnectionError
from prettytable import PrettyTable
from collections import OrderedDict
from datetime import datetime

from .utils import colored, BaseError, ValueInvalidError, ResourceNotFoundError

from pprint import pprint

QUERY_URL = 'https://kyfw.12306.cn/otn/lcxxcx/query'


# Tickets data collector
class TicketsCollector(object):
    '''
    A set of raw datas from TicketsQuery
    rows: data from query 12306
    opts: show fliters with command line options
    '''

    
    def __init__(self, rows, opts):
        self._rows = rows
        self._opts = opts


    def __repr__(self):
        return '<Trains size=%s>' %(len(self))


    def __iter__(self):
        i = 0
        while True:
            if i < len(self):
                yield self[i]
            else:
                yield next(self)
            i += 1


    def __len__(self):
        return len(self._rows)



    # 历时
    def _get_duration(self, row):
        duration = row.get('lishi').replace(':', '小时') + '分钟'
        # 不足小时,只显示分钟
        if duration.startswith('00'):       
            return duration[4:]
        # 不足10小时,小时只显示一位
        if duration.startswith('0'):
            return duration[1:]
        return duration



    @property
    def trains(self):
        '''
        Filter rows according to `headers`
        '''
        for row in self._rows:
            # 车次
            train_code = row.get('station_train_code')
            initial = train_code[0].lower() # 车次第一位就是车的型号

            # 根据opts显示数据,默认全部显示
            if not self._opts or initial in self._opts:
                train = [
                        # 车次
                        train_code,
                        # 车站      
                        '\n'.join([
                            colored.red(row.get('from_station_name')), 
                            colored.green(row.get('to_station_name'))]),
                        # 时间
                        '\n'.join([
                            colored.red(row.get('start_time')), 
                            colored.green(row.get('arrive_time'))]),
                        # 历时
                        self._get_duration(row),
                        # 商务
                        row.get('swz_num'),
                        # 一等
                        row.get('zy_num'),
                        # 二等
                        row.get('ze_num'),
                        # 软卧
                        row.get('rw_num'),
                        # 硬卧
                        row.get('yw_num'),
                        # 软座
                        row.get('rz_num'),
                        # 硬座
                        row.get('yz_num'),
                        # 无座
                        row.get('wz_num')
                    ]
                yield train

    
    # show data
    def pretty_print(self):
        '''
        Use PrettyTable to perform formatted outprint
        '''
        
        # 格式化显示数据
        headers = '车次 车站 时间 历时 商务 一等 二等 软卧 硬卧 软座 硬座 无座'.split()
        pt = PrettyTable()
        if len(self) == 0:
            pt._set_field_names(['Sorry,'])
            pt.add_row(['Train not find'])
        else:
            pt._set_field_names(headers)
            for train in self.trains:
                pt.add_row(train)
        print(pt)

 

# Request data
class TicketsQuery(object):

    def __init__(self, from_station, to_station, date, opts=None):
        self.from_station = from_station
        self.to_station = to_station
        self.date = date
        self.opts = opts

    def __repr__(self):
        return 'TrainTicketsQuery from=%s to=%s date=%s' %(self.from_station, self.to_station, self.date)

    
    @property
    def _stations(self):
        # 导入站点
        d = {}
        datapath = os.path.join(os.path.dirname(__file__), 'data')
        sys.path.append(datapath)
        mod = __import__('stations', globals(), locals())
        d =  mod.stations
        return d

    @property
    def _from_station_telecode(self):
        code = self._stations.get(self.from_station)
        if not code:
            ResourceNotFoundError('from_station_telecode', 'Can\'t find the telecode of from_station').exit_after_echo()
        return code
    
    @property
    def _to_station_telecode(self):
        code = self._stations.get(self.to_station)
        if not code:
            ResourceNotFoundError('from_station_telecode', 'Can\'t find the telecode of to_station').exit_after_echo()
        return code

    @property
    def _date(self):
        result = re.findall('\d+', self.date)
        length = len(result)    # length should be 2 or 3
        
        date_str = ''
        if length == 2:
            year = datetime.today().year
            # Auto add year
            date_str = ''.join(result) + str(year)
        elif length == 3:
            date_str = ''.join(result)
        else:
            # print(result)
            ValueInvalidError('date', 'Input date is invalid, format maybe error').exit_after_echo()
        
        if not date_str:
            ValueInvalidError('date', 'Date can\'t be empty').exit_after_echo()

        try:
            date = datetime.strptime(date_str, '%Y%m%d')
        except ValueError:
            ValueInvalidError('date', 'Input date format is invalid').exit_after_echo()
        # 12306 can only query within 50 days
        offset = date - datetime.today()
        if offset.days not in range(-1, 50):
            ValueInvalidError('date', 'Input date is invalid, just can only within 50 days from today').exit_after_echo()
            
        # Generate valid date for query 
        return datetime.strftime(date, '%Y-%m-%d')
    

    # build params for requests
    def _build_params(self):
        d = OrderedDict()
        d['purpose_codes'] = 'ADULT'
        d['queryDate'] = self._date
        d['from_station'] = self._from_station_telecode
        d['to_station'] = self._to_station_telecode
        return d

    
    def query(self):
        params = self._build_params()

        try:
            r = requests.get(QUERY_URL, params=params, verify=False)
        except ConnectionError:
            BaseError('Network', 'Network connection fail').exit_after_echo()
        
        try:
            rows = r.json()['data']['datas']
        except KeyError:
            rows = []
        except TypeError:
            ResourceNotFoundError('response', 'No response').exit_after_echo()
        
        return TicketsCollector(rows, self.opts)
