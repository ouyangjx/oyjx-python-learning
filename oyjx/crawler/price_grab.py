# coding:utf-8 # 防止通过命令行执行Python程序时报错如：Non-ASCII character '\xe4'之类

from urllib import error
import json
import requests
import logging
from some_func import *

# 任务

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG)

email = 'ouyangjx145@gmail.com'
account = 'oyjx'
password = 'xxxx'
buyer_login_url = 'https://backend.gamivo.com/api/user/sign-in'

headers = {
    'accept': 'application/json, text/plain, */*',
    'content-type': 'text/plain',  # 'application/json' # 用这个也可以
    'referer': 'https://www.gamivo.com/login',
    'origin': 'https://www.gamivo.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}
account_info = {'email': account, 'password': password, 'captcha': ''}

"""
logging.debug('爬虫：')
try:
    response = request.urlopen('https://www.gamivo.com/product/lords-of-the-fallen-goty',timeout=10)  # timeout=10
    content = response.read().decode('utf-8')
    soup = BeautifulSoup(content, 'lxml')
    lowest_price_item = soup.select('#lowest-price')  # €&nbsp;
    
    # Demo
    # items1 = soup.select("div.author a img")
    # items2 = soup.select("a div.content span")
    # items3 = soup.select("div.thumb a img")
    
    print('length：' + str(len(lowest_price_item)))
    lowest_price_str = lowest_price_item[0].text
    print('lowest_price_str：' + lowest_price_str)
    price_item = lowest_price_str.split('€ ')
    if len(price_item) > 1:
        price = price_item[1]
        print('price：' + price)
    else:
        print('error rice!')
except error.HTTPError as e: # from urllib import request, error
    print(e.reason, e.code, e.headers, sep='\n')
except error.URLError as e:
    print(type(e.reason))
    if isinstance(e.reason, socket.timeout):
        print('TIME OUT')
"""

"""
filename = 'cookie.txt'
cookie = http.cookiejar.MozillaCookieJar(filename)
handler = request.HTTPCookieProcessor(cookie)

# 可以选择而是用代理服务器地址
# proxy_addr = '61.163.39.70:9999'
# proxy = request.ProxyHandler({'http': proxy_addr})
# opener = request.build_opener(proxy, handler)

opener = request.build_opener(handler)

# 将opener安装为全局
request.install_opener(opener)

# 因为请求参数是Request payload；content-type是text/plain，故下面这种方式不适用
data = bytes(parse.urlencode(account_info), encoding='utf8')  # from urllib import request, parse
request_obj = request.Request(url=buyerLoginUrl, data=data, headers=headers, method='POST')
response = request.urlopen(request_obj)
print(response.read().decode('utf-8'))

for item in cookie:
    print(item.name+'='+item.value)
cookie.save(ignore_discard=True, ignore_expires=True)
"""

"""
cookies_file_path = '/home/oyjx/Documents/cookies.txt'

fHandle = open(cookies_file_path, 'r')
cookies_str = fHandle.read()
if cookies_str == '':
    response = requests.post(buyerLoginUrl, data=json.dumps(account_info), headers=headers)
    # 更新cookies
    cookies_str = update_cookies(response, cookies_file_path)

print(cookies_str)

# 拿到cookie信息请求其他url
cookies = {}
if cookies_str != '':
    for item in cookies_str.strip().split(";"):
        if item == '':
            continue
        array = item.strip().split('=')
        cookies[array[0]] = array[1]

    print(cookies)

    # 这是另一个域了
    profile_settings_url = "https://backend.gamivo.com/api/profile/settings"
    response = requests.get(profile_settings_url, headers=headers, cookies=cookies)
    # 更新cookies
    cookies_str = update_cookies(response, cookies_file_path)
    response_json = response.json()
    if response.status_code != 200:
            try:
                message = response_json.get('errors')[0].get('message')
                if message == 'Access Denied.':
                    print("需要重新登录！")
                else:
                    print(message)
            except error as e:
                print(e.reason, e.code, e.headers, sep='\n')
    else:
        print(response_json)
else:
    print('无法登录！')

"""

logging.debug("真正实现：")

"""
根据网站的情况，就不拿cookie了，因为它是与主域名和其他域名的，用户登录信息并非通过cookie存储
用户信息域：.backend.gamivo.com
登录成功返回：x-token=xxxx
下次请求带上（登录时放在了Local Storage里的token）：x-gamivo-auth=xxxx
放在Local Storage的还有登录返回的用户信息user和_lr_id_（userID）（这个不知道是不是取自user里的id生成的）
"""

def login(login_url, the_account_info, the_headers):
    """

    :param login_url: 登录url
    :param the_account_info: 参数信息
    :param the_headers: header信息
    :return: 最新的token
    """
    logging.debug(json.dumps(the_account_info))
    the_account = the_account_info.get('email')
    x_token = ""
    try:
        the_response = requests.post(login_url, data=json.dumps(the_account_info), headers=the_headers, timeout=10)

        if the_response.status_code == 200:
            # 从请求头获取x-token
            x_token = the_response.headers.get('x-token')

            # >更新token（使用.txt文件存储）
            # update_token(the_account, x_token, tokenFilePath)

            # >更新token（新方法，使用.pickle文件存储）
            update_token_new(the_account, x_token, token_file_path)
        else:
            # @Todo
            the_response_json = the_response.json()
            the_message = the_response_json.get('errors')[0].get('message')
            logging.error(the_message)
    except error as e_:
        logging.error(e_.reason, e_.code, e_.headers, sep='\n')

    return x_token


# >获取旧token（使用.txt文件存储）
# token = ''
# token_file_path = '/home/oyjx/Documents/token.txt'
# token_file_path = 'token.txt'
# file_handle = open(token_file_path, 'r')
# token_list_str = file_handle.read()
# if token_list_str != '':
#     token = get_key_value_of_str(token_list_str, dict.get('email'))


# >获取旧token（新方法，使用.pickle文件存储）
token_file_path = 'token.pickle'
token = get_old_token_new(account_info.get('email'), token_file_path)

if token == '' or token is None:
    token = login(buyer_login_url, account_info, headers)

logging.debug(token)

# 拿到token请求其他url
if token != '' and token is not None:
    # profile_settings_url = "https://backend.gamivo.com/api/profile/settings"
    profile_settings_url = "https://backend.gamivo.com/api/profile/me"                                                                                                                                                                                                                                        seller

    # 通过在请求头传递x-gamivo-auth
    # headers['x-gamivo-auth'] = token
    try:
        response = requests.get(profile_settings_url, headers=headers, timeout=10)
        response_json = response.json()
        if response.status_code == 200:
            # logging.debug('email:' + response_json.get('email'))
            logging.debug(response_json)
        else:
            message = response_json.get('errors')[0].get('message')
            logging.error(message)
            # 重新登录
            token = login(buyer_login_url, account_info, headers)
    except error as e:
        logging.error(e.reason, e.code, e.headers, sep='\n')
else:
    logging.error('无法登录！')
