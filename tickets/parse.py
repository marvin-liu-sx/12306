# -*- coding:utf-8 -*-

import re
from pprint import pprint

'''
parse stations.html for getting stations' code
'''

with open('stations.html') as f:
    # read all the content from file
    text = f.read()

# \u4e00 - \u9fa5：汉字区间
# 汉字|A-Z  构成一个站点及其缩写代码
# findall返回一个列表，列表中每个元素是一个元组，每个元组由正则表达式中的()表示的子表达式匹配的结果构成
stations = re.findall(r'([\u4e00-\u9fa5]+)\|([A-Z]+)', text)

# print(type(stations))

# print(stations[10])

pprint(dict(stations), indent=4)
