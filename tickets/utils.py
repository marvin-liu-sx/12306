# -*- coding:utf-8 -*-

import sys


# Print text color 
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


# Exception handlers
class BaseError(Exception):
    '''
    The base error contains error(required), data(optional) and message(optional)
    '''
    def __init__(self, error, data='', message=''):
        super(BaseError, self).__init__(message)
        self.error = error
        self.data = data
        self.message = message
    
    
    def exit_after_echo(self, color='red'):
        if color == 'red':
            print(colored.red(self.message))
        else:
            print(self.message)
        exit()


class ValueInvalidError(BaseError):
    '''
    Indicate the input has error or invalid. The data specifices the error field of input form
    '''
    def __init__(self, field, message=''):
        super(ValueInvalidError, self).__init__('Value:invalid', field, message)


class ResourceNotFoundError(BaseError):
    '''
    Indicate the resource was not found. The data specifices the resource name
    '''
    def __init__(self, field, message=''):
        super(ResourceNotFoundError, self).__init__('Resource:not found', field, message)

