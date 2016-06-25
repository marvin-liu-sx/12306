# -*- coding:utf-8 -*-

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

from docopt import docopt
import requests
from prettytable import PrettyTable

from stations import stations
from utils import colored



def cli():
    '''
    command-line interface
    '''
    # 获得命令行参数
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']

    # 构建url
    url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'.format(date, from_station, to_station)
    
    # 发起请求
    r = requests.get(url, verify=False)
    
    # 获取返回数据
    # print(r.json())
    rows = r.json()['data']['datas']

    # 格式化显示数据
    headers = '车次 车站 时间 历时 商务 一等 二等 软卧 硬卧 软座 硬座 无座'.split()
    pt = PrettyTable()
    pt._set_field_names(headers)
    for row in rows:
        # 车次
        train_code = row.get('station_train_code')
        # 车站
        from_station_name = colored.red(row.get('from_station_name'))
        to_station_name = colored.green(row.get('to_station_name'))
        station = '\n'.join([from_station_name, to_station_name])
        # 时间
        start_time = colored.red(row.get('start_time'))
        arrive_time = colored.green(row.get('arrive_time'))
        time = '\n'.join([start_time, arrive_time])
        # 历时
        duration = row.get('lishi').replace(':', '小时') + '分钟'
        # 商务
        swz_num = row.get('swz_num')
        # 一等
        ydz_num = row.get('zy_num')
        # 二等
        edz_num = row.get('ze_num')
        # 软卧
        rw_num = row.get('rw_num')
        # 硬卧
        yw_num = row.get('yw_num')
        # 软座
        rz_num = row.get('rz_num')
        # 硬座
        yz_num = row.get('yz_num')
        # 无座
        wz_num = row.get('wz_num')
        pt.add_row([train_code, station, time, duration, swz_num, ydz_num, edz_num, rw_num, yw_num, rz_num, yz_num, wz_num])

    print(pt)


if __name__ == '__main__':
    cli()


