#__coding__:'utf-8'
#auther:ly
import re
from kx_api.common.reflex import Reflex
def  re_replace(target):
    '''
    该函数主要是使用正则完成测试用例中params参数的替换
    re.search当找到和p规则匹配的数据就返回，返回一个对象，true
    m.group()等同于group(0)函数,返回的是匹配的整个字符串#括号里面的#
    m.group(1)返回的是匹配的第一个括号里面的字符串'''
    p='#(.*?)#'
    while re.search(p,target):
        m=re.search(p,target)
        key = getattr(Reflex,m.group(1))
        #每替换一次就将最新的字符串赋值给taget
        target =re.sub(p,key,target,count=1)
    return target

def findId(target,key,value):
    '''
    此方法主要是用来根据上一步骤的id，查找与之相关联的id
    :param target: 请求返回的结果
    :param key: 查看的字段
    :param value: 查找的字段的值
    :return: i ,找到了就直接返回整个字典
    '''
    for i in target:
        if i[key] == value:
            return i



if __name__ == '__main__':
    pass