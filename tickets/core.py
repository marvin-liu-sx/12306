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
from .trains import QUERY_URL, TicketsCollector, TicketsQuery   # can only run scripts from outside
from pprint import pprint

def run_query():
    
    # 获得命令行参数
    arguments = docopt(__doc__)
    from_station = arguments['<from>']
    to_station = arguments['<to>']
    date = arguments['<date>']
    opts = []
    for k in arguments.keys():
        if arguments[k] is True:
            opts.append(k[1])
    
    test_query = TicketsQuery(from_station, to_station, date, opts)
    test_query.query().pretty_print()

if __name__ == '__main__':
    run_query()

