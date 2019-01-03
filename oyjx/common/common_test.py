"""
测试通用方法
"""


# 判断是执行当前模块
def is_exec_curr(exec_list, directory_index):
    """

    :param exec_list:需执行模块目录下标列表
    :param directory_index:当前模块目录下标
    :return:是否需要执行当前模块
    """
    # 如果包含0则表示需要执行所有模块，返回True
    if 0 in exec_list:
        return True

    if directory_index in exec_list:
        return True

    return False

