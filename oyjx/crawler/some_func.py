import pickle
import os


def update_cookies(response, cookies_file_path):
    """

    :param response: 响应的response对象
    :param cookies_file_path: 存放cookie的文件夹的地址
    :return:
    """
    cookies = response.cookies
    if len(cookies) == 0:
        return
    cookies_str = ''
    for item in cookies:
        cookies_str = cookies_str + item.name + '=' + item.value + ';'
    f_handle = open(cookies_file_path, 'wb')
    f_handle.write(bytes(cookies_str, encoding='utf8'))
    f_handle.close()
    return cookies_str


def get_str_dict(str):
    """

    :param str: 字符串
    :return: 字典
    """
    str_dict = {}

    if str != '':
        str_list = str.strip().split(';')
        for item in str_list:
            if item == '':
                continue
            item_list = item.strip().split('=')
            the_key = item_list[0]
            the_val = item_list[1]
            str_dict[the_key] = the_val

    return str_dict


def get_key_value_of_str(str, key):
    """

    :param str: 字符串
    :param key: 键
    :return: 键值
    """
    str_dict = get_str_dict(str)
    return str_dict.get(key)


def update_key_value_of_str(str, key, val):
    """

    :param str: 字符串
    :param key: 键
    :param val: 新值
    :return: 新字符串
    """

    str_dict = get_str_dict(str)

    if str_dict.get(key) == val:
        return str

    str_dict[key] = val

    str_new = ''
    for key in str_dict.keys():
        str_new = str_new + key + '=' + str_dict[key] + ';'

    print(str_new)

    return str_new


def update_token(account, token, token_file_path):
    """

    :param account: 账号
    :param token: 新token
    :param token_file_path: 存放token的文件夹的地址
    :return:

    """
    if token == '' or token is None:
        return
    if account == '' or account is None:
        return
    if token_file_path == '' or token_file_path is None:
        return

    f_handle = open(token_file_path, 'r')
    token_old = f_handle.read()

    token_new = update_key_value_of_str(token_old, account, token)

    if token_old == token_new:
        return

    f_handle = open(token_file_path, 'wb')
    f_handle.write(bytes(token_new, encoding='utf8'))
    f_handle.close()


# 利用pickle
def update_token_new(account, token, token_file_path):
    """

    :param account: 账号
    :param token: 新token
    :param token_file_path: 存放token的pickle
    :return:

    """
    if token == '' or token is None:
        return
    if account == '' or account is None:
        return
    if token_file_path == '' or token_file_path is None:
        return

    token_datas = {}

    """
    涉及的问题：如果手动建立一个空pickle文件，那么open之后得到的read_token_data无法载入到字典
        1、完全通过程序创建pickle文件，并写入空字典
        2、每次读取pickle文件之后判断下是否有数据，没有则写入空字典（好不优雅）
        3、
    """

    # 1、可以考虑只能通过程序来创建文件（不存在则创建并写入空字典{}，完全不能人为修改文件）
    if not os.path.exists(token_file_path):
        with open(token_file_path, 'wb') as write_token_data:
            pickle.dump(token_datas, write_token_data)

    with open(token_file_path, 'rb') as read_token_data:

        # 2、判断文件是否有数据，先调用read()方法看得到的len()是否大于0
        # @Todo 每次都这样判断，不是很优雅
        if len(read_token_data.read()) <= 0:
            with open(token_file_path, 'wb') as write_token_data:
                pickle.dump(token_datas, write_token_data)
        else:
            # 前面调用了read()方法，需要调用seek(0)，才能从开始行重新加载
            read_token_data.seek(0)
            token_datas = pickle.load(read_token_data)
        if token_datas is None or len(token_datas) <= 0:
            token_datas = {}

    print(token_datas)

    if token_datas.get(account) == token:
        return

    token_datas[account] = token

    with open(token_file_path, 'wb') as write_token_data:
        pickle.dump(token_datas, write_token_data)


# 利用pickle
def get_old_token_new(account, token_file_path):
    """

    :param account: 账号
    :param token_file_path: 存放token的pickle
    :return:

    """
    if account == '' or account is None:
        return ''
    if token_file_path == '' or token_file_path is None:
        return ''

    with open(token_file_path, 'rb') as read_token_data:
        token_datas = pickle.load(read_token_data)
        if token_datas is None or len(token_datas) <= 0:
            token_datas = {}

    print(token_datas)

    return token_datas.get(account)


# 模块被导入时，if里面的代码不会运行
if __name__ == '__main__':
    # Test
    # update_token('a', 'b', 'token.txt')  # '/home/oyjx/Documents/token.txt'

    # Test 利用pickle
    update_token_new('oyjx', '5k96rzqcnow8cockccowwoc0cow0ssk0g88s88c4c88cgw0s8s', 'token.pickle')  # '/home/oyjx/Documents/token.pickle'
    get_old_token_new('oyjx', 'token.pickle')  # '/home/oyjx/Documents/token.pickle'
