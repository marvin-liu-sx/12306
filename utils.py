# -*- coding:utf-8 -*-

import sys

def exit_after_echo(msg, color='red'):
    if color == 'red':
        print(colored.red(msg))
    else:
        print(msg)
    exit()


class Colored(object):
    
    RED = '\033[91m'    # 设置console黑底深红色
    GREEN = '\033[92m'  # 设置console黑底绿色

    DEFAULT = '\033[0m' # 默认关闭console的设置属性
    
    def color_str(self, color, s):
        return '%s%s%s' %(getattr(self, color), s, self.DEFAULT)

    def red(self, s):
        return self.color_str('RED', s)

    def green(self, s):
        return self.color_str('GREEN', s)


colored = Colored()
