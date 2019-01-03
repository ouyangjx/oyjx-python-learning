import os
import socket
from http import cookiejar
from urllib import request, error, parse
from urllib.parse import urlparse, urlunparse, urljoin, urlencode
from bs4 import BeautifulSoup
import lxml


# 1、urlparse
# 用法：urllib.parse.urlparse(urlstring, scheme='', allow_fragments=True)
print('\n1、urlparse：')
result = urlparse('http://www.baidu.com/index.html;user?id=5#comment')
print(type(result), result)

result = urlparse('www.baidu.com/index.html;user?id=5#comment', scheme='https')
print(result)

result = urlparse('http://www.baidu.com/index.html;user?id=5#comment', scheme='https')
print(result)

result = urlparse('http://www.baidu.com/index.html;user?id=5#comment', allow_fragments=False)
print(result)

result = urlparse('http://www.baidu.com/index.html#comment', allow_fragments=False)
print(result)

# 2、urlunparse @Todo
print('\n2、urlunparse：')
data = ['http', 'www.baidu.com', 'index.html', 'user', 'a=6', 'comment']
print(urlunparse(data))

# 3、urljoin
print('\n3、urljoin：')
print(urljoin('http://www.baidu.com', 'FAQ.html'))
print(urljoin('http://www.baidu.com', 'https://cuiqingcai.com/FAQ.html'))
print(urljoin('http://www.baidu.com/about.html', 'https://cuiqingcai.com/FAQ.html'))
print(urljoin('http://www.baidu.com/about.html', 'https://cuiqingcai.com/FAQ.html?question=2'))
print(urljoin('http://www.baidu.com?wd=abc', 'https://cuiqingcai.com/index.php'))
print(urljoin('http://www.baidu.com', '?category=2#comment'))
print(urljoin('www.baidu.com', '?category=2#comment'))
print(urljoin('www.baidu.com#comment', '?category=2'))

# 4、urlencode
print('\n4、urlencode：')
params = {
    'name': 'oyjx',
    'age': 0
}
base_url = 'http://www.baidu.com?'
url = base_url + urlencode(params)
print(url)

# urlopen
# 用法：urllib.request.urlopen(url, data=None, [timeout, ]*, cafile=None, capath=None, cadefault=False, context=None)
print('\n5、urlopen：')

# image
print('\nurlopen of image：')
# image_test = 'http://wsimg.szlcsc.com/upload/product/desc_img/2016-12-18/e54ce45b279f479093e010f645ae2474.jpg'
# request.urlretrieve(image_test, 'usr/local/image_test.jpg')


# html
print('\nurlopen of html：')

"""
try:
    
    # form表单参数
    data = {
        'catalogNodeId': 11047,
        'totalCount': 52,
        'type': 'catalog',
        'catalogName': '%E4%BC%A0%E6%84%9F%E5%99%A8%E6%A8%A1%E5%9D%97',
        'queryProductStandard': '',
        'queryProductArrange': '',
        'pageAddSearchRecord': 1,
        'queryProductGradePlateId': '',
    }
    data = bytes(parse.urlencode(data), encoding='utf8')
    url = 'https://list.szlcsc.com/addSearchRecord.html';
    response = request.urlopen(url, data)
    print(response.read().decode('utf-8'))

    response = request.urlopen('https://www.szlcsc.com', timeout=5)
    print('response type（响应类型）：' + str(type(response)))
    print('response status（状态码）：' + str(response.status))
    print('response headers（响应头）：' + str(response.getheaders()))
    print('response headers of Server：' + str(response.getheader('Server')))

    # 读取一行内容
    data_line=response.readline().decode('utf-8')
    print(data_line)

    # 读取所有内容
    print(response.read().decode('utf-8'))
    data = response.read()
    # 打开文件，没有则创建（w：写；b：二进制）
    fHandle = open('/home/oyjx/Documents/test.html', 'wb')
    # 将爬取的网页保存在本地
    fHandle.write(data)
    fHandle.close()
    # @Todo python I/O相关操作参考：https://www.cnblogs.com/juandx/p/4962089.html
except error.HTTPError as e:  # from urllib import request, error
    print(e.reason, e.code, e.headers, sep='\n')
except error.URLError as e:
    print(type(e.reason))
    if isinstance(e.reason, socket.timeout):
        print('TIME OUT')
else:
    print('Request Successfully!')
"""

# Request @Todo
print('\n6、Request：')

"""
request = request.Request('https://python.org')
response = request.urlopen(request)
print(response.read().decode('utf-8'))


url = 'http://httpbin.org/post'
headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Host': 'httpbin.org'
}
dict = {
    'name': 'oyjx'
}
data = bytes(parse.urlencode(dict), encoding='utf8') # from urllib import request, parse
req = request.Request(url=url, data=data, headers=headers, method='POST')
response = request.urlopen(req)
print(response.read().decode('utf-8'))


url = 'http://httpbin.org/post'
dict = {
    'name': 'oyjx'
}
data = bytes(parse.urlencode(dict), encoding='utf8')
req = request.Request(url=url, data=data, method='POST')
req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
req.add_header('Host', 'httpbin.org')
response = request.urlopen(req)
print(response.read().decode('utf-8'))
"""

# proxy @Todo
print('\n7、proxy：')
"""
proxy_handler = request.ProxyHandler({
    'http': 'http://127.0.0.1:9743',
    'https': 'https://127.0.0.1:9743'
})
opener = request.build_opener(proxy_handler)
response = opener.open('http://httpbin.org/get')
print(response.read())
"""

# Cookie @Todo
print('\n8、cookie：')
"""
cookie = http.cookiejar.CookieJar() # import http.cookiejar
handler = request.HTTPCookieProcessor(cookie)
opener = request.build_opener(handler)
response = opener.open('http://www.baidu.com')
for item in cookie:
    print(item.name+'='+item.value)


filename = 'cookie.txt'
cookie = http.cookiejar.MozillaCookieJar(filename)
handler = request.HTTPCookieProcessor(cookie)
opener = request.build_opener(handler)
response = opener.open('http://www.baidu.com')
cookie.save(ignore_discard=True, ignore_expires=True)
"""

# Python urllib的urlretrieve()函数解析 (显示下载进度)
# https://www.cnblogs.com/alamZ/p/7099178.html
print('\n9、urlretrieve：')

"""
def schedule(a, b, c):
    # a: 已经下载的数据块
    # b: 数据块的大小
    # c: 远程文件的大小
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    # 有时间改成横向的
    print('%.2f%%' % per)


# 下载资源并使用Schedule函数显示下载进度
# url = 'http://www.python.org/ftp/python/2.7.5/Python-2.7.5.tar.bz2'
url = 'https://www.baidu.com/img/bd_logo1.png'
params = url.split('/');
file_name = params[len(params) - 1]
local = os.path.join('/home/oyjx/Documents', file_name)  # import os
request.urlretrieve(url, local, schedule)
"""

# 使用BeautifulSoup，需要安装python-bs4，然后在File>Settings>Project Interpreter添加软件包
print('\n10、bs4：')

""""
response = request.urlopen('https://www.gamivo.com/product/lords-of-the-fallen-goty', timeout=5)
url = 'http://www.qiushibaike.com/'
print(url)
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
req = request.Request(url, headers={
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
})
response = request.urlopen(req)
content = response.read().decode('utf-8')
# print(content)
soup = BeautifulSoup(content, 'lxml')
items1 = soup.select('div.author a img')
items2 = soup.select('a div.content span')
items3 = soup.select('div.thumb a img')
n = 0
length1 = len(items1)
length3 = len(items3)
while n < length1:
    print('作者信息：\n名称：'+items1[n]['alt']+'\n头像链接：'+items1[n]['src']+'\n\n')
    print('段子信息：\n段子：'+items2[n].text+'\n')
    # 以免有些没有图片的段子报错
    if n < length3:
        print('段子图片链接：'+items3[n]['src']+'========================================')
    else:
        print('========================================')
    n += 1
"""

# split操作没有字符串中没有匹配符则返回数组只有一个元素就是原来的字符串；如果匹配到了，且在匹配符在字符串开头，则会有一个''元素
print('\nsplit：')
content = '€ 4.92'
content_ = '>€ 4.92'
print('content：' + content)
print('content_：' + content_)
print(content.split('$'))
print(content.split('€ '))  # 注意这个' '不是普通的空格' '！！！
print(content_.split('€ '))
if len(content.split('€ ')) > 1:
    print(content.split('€ ')[1])
    print(content_.split('€ ')[1])
else:
    print('error!')
