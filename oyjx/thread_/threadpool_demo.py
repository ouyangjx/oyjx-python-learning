import sys
import threadpool
sys.path.append("..")
from common.common_test import *
"""
参考：
    忘了哪个网站了
    《Python 核心编程》
目录：
    1、使用threadpool
    2、threading_demo.py使用的concurrent.future下的ThreadPoolExecutor
    ...
"""

# 可以指定1-7执行哪些程序，或者指定为[0]执行全部
exe_list = [0]

print('1、使用threadpool')


def func(num):
    print('num:' + repr(num))


if is_exec_curr(exe_list, 1) and __name__ == '__main__':
    res = list(range(100))
    pool = threadpool.ThreadPool(20)  # 20个线程
    requests = threadpool.makeRequests(func, res)  # 生成线程要执行的所有线程,第一个参数为函数名，第二个参数是传的值
    for request in requests:
        pool.putRequest(request)
    # [pool.putRequest(request) for request in requests]  # 与上面的for循环等价
    pool.wait()  # 等待，其他线程执行结束
