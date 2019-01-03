import sys
import random
import os
import copy
import pickle
import math


class HelloWorld:
    def __init__(self):
        self.say = 'Hello,world!'
        self.worlds = ['Hello', 'world']

    def say_hello_world(self):
        return self.say


# My first python program
helloWorld = HelloWorld()

# 0、一些
print('\n0、一些：')

print('Python version:', sys.version_info)

print("information of %s:\nname:%s\nage:%s\nsex:%s" % ('oyjx', 'oyjx', '18', '18'))

print('''
information of %s:
name:%s
age:%s
sex:%s
''' % ('oyjx', 'oyjx', '18', '男'))

# 1、变量和方法
print('\n1、变量和方法')

print(helloWorld.say)

print(helloWorld.say_hello_world())

# 2、列表
print('\n2、列表')

# 列表取值（和数组类似）
# @注：python的数值类型不能直接和字符串相加，如想转成字符串，可用str()方法
print('length:' + str(len(helloWorld.worlds)) + ';content:' + helloWorld.worlds[0] + ',' + helloWorld.worlds[1] + '!')

# 列表相关操作 append在最后面追加、extend可追加一个列表、insert插入到指定下标
print('\n列表相关操作：')

# 追加
helloWorld.worlds.append('test1')
print(helloWorld.worlds)

print(helloWorld.worlds + ['test666'])

# 继承
helloWorld.worlds.extend(['test2', 'test3'])
print(helloWorld.worlds)

# 按下标插入
helloWorld.worlds.insert(2, 'test4')
print(helloWorld.worlds)

# 截取
print(helloWorld.worlds[0:3])
print(helloWorld.worlds[1:7])

# 列表遍历
print('\n列表遍历：')
for world in helloWorld.worlds:
    print(world)

# isinstance()方法判断数据类型
print('\nisinstance()方法：')
list_test = ['oyjx', ['175', '120', ['eat', 'sleep', 'reading', 'and so on']], 'ouyangjx']

for item in list_test:
    if isinstance(item, list):
        for item_ in item:
            if isinstance(item_, list):
                for item__ in item_:
                    print(item__)
            else:
                print(item_)
    else:
        print(item)

# 递归实现列表遍历（注意点：Python3默认认为递归深度不能超过100，但是可以修改这个深度上限）
print('\n递归实现列表遍历：')


def foreach_list(the_list, indent=False, level=None):
    if level is None:
        level = 0

    for the_item in the_list:
        if isinstance(the_item, list):
            foreach_list(the_item, indent, level + 1)
        else:
            if indent:
                # for i in range(deep):
                #     print('\t', end='')
                print('\t' * level, end='')
            print(the_item)


foreach_list(list_test)
print()
foreach_list(list_test, True)
print()
foreach_list(list_test, True, 1)


print("\n深浅拷贝：")
copy_src = [[5, 1], 1, 0, 2]
reference_a = copy_src
copy_b = copy.copy(copy_src)
deep_copy_c = copy.deepcopy(copy_src)

copy_src.append(4)
copy_src[0].append(2)

print(copy_src)
print(reference_a)
print(copy_b)
print(deep_copy_c)

deep_copy_c.pop(0)
copy_b[0].extend([1, 0, 2, 4])
reference_a.extend([5, 1, 2])

print(copy_src)
print(reference_a)
print(copy_b)
print(deep_copy_c)



# 3、共享代码
print('\n3、共享代码：')

# BIF（内置函数）
"""
list() 这是一个工厂函数，创建一个新的空列表
range() 返回一个迭达器，根据需要生成一个指定范围的数字
    list(range(0, 2)) 返回 [0, 1]
    list(range(2)) 返回 [0, 1]
    list(range(0, -1, -1)) 返回0
enumerate() 创建成对数据的一个编号列表，从0开始
int() 将一个字符串或另一个数据换为一个整数（如果可行）
id() 函数用于获取对象内存地址（Python对象的唯一标识）
next() 返回一个可迭代数据结构（如列表）中的下一项
"""
print('\nBIF（内置函数）：')
# 一些关于Python随机数random和range()内置函数的测试
languages = ['Java', 'Python', 'C', 'C++', 'R', 'Ruby']
print('random.randint1:' + languages[random.randint(0, len(languages) - 1)])
print('random.randint2:' + random.choice(languages))

# 产生 1 到 10 的一个整数型随机数
print(random.randint(1, 10))
# 产生 0 到 1 之间的随机浮点数
print(random.random())
# 产生  1.1 到 5.4 之间的随机浮点数，区间可以不是整数
print(random.uniform(1.1, 5.4))
# 从序列中随机选取一个元素
print(random.choice('tomorrow'))
# 生成从1到100的间隔为2的随机整数
print(random.randrange(1, 100, 2))

# __len__()和len()的区别？


# 4、文件与异常
print('\n4、文件与异常')

# 当前工作目录是什么
print(os.getcwd())

# 切换目录
os.chdir('../io')
print(os.getcwd())

sketch_file = 'sketch.txt'

data = open(sketch_file)
print()
print(data.readline(), end='')
print(data.readline(), end='')

# 返回到文件起始位置
data.seek(0)

print('\n通过特殊处理：')
for each_line in data:
    print(each_line, end='')
    # split的可选参数maxsplit设置为1，则被分割符分割后之得到两份
    # if not each_line.find(':') == -1:
    if each_line.find(':') != -1:
        (index, value) = each_line.strip().split(':', 1)
        print(index, end='')
        print(' is ', end='')
        print(value)

# 通过异常处理
print('\n\n通过异常处理：')
data.seek(0)
for each_line in data:
    try:
        print(each_line.strip())
        (index, value) = each_line.strip().split(':')
        print(index, end='')
        print(' is ', end='')
        print(value)
    except ValueError as e:
        print('Error:' + str(e))
        # 忽略错误
        pass

print('\n\n如果文件不存在：')

test_file = 'test.txt'

print('\n手动判断处理：')
if os.path.exists(test_file):
    data = open(test_file)
else:
    print('File ' + test_file + ' is not found.')

print('\n通过异常处理：')
try:
    data = open(test_file)
# 通过Exception可以捕获所有异常   except:
# except Exception as e:
except FileNotFoundError as e:
    print('Error:' + str(e))

data.close()

# 5、持久存储
print('\n5、持久存储：')

index_data = []
value_data = []
index_value_data = {}
if os.path.exists(sketch_file):
    data = open(sketch_file)
    for each_line in data:
        try:
            print(each_line, end='')
            (index, value) = each_line.strip().split(':', 1)
            index_data.append(index)
            value_data.append(value)
            index_value_data[index] = value
        except ValueError as e:
            print('Error:' + str(e))
            # 忽略错误
            pass
else:
    print('File ' + sketch_file + ' is not found.')

print()
print(index_data)
print(value_data)
print(index_value_data)

print('\n以写模式打开文件：')
index_data_file = None
value_data_file = None
index_value_data_file = None
try:
    # 以写模式打开文件（如果文件不存在则会创建）
    index_data_file = open('index_data.txt', 'w')
    value_data_file = open('value_data.txt', 'w')
    index_value_data_file = open('index_value_data.txt', 'w')

    # 使用print()将指定的数据保存到指定的磁盘文件，当然也可以使用文件对象的write方法
    print(index_data, file=index_data_file)
    print(value_data, file=value_data_file)
    print(index_value_data, file=index_value_data_file)

    # 关闭文件，最好移到finally组
    # index_data_file.close()
    # value_data_file.close()
    # index_value_data_file.close()
except IOError as e:
    print('Error:' + str(e))
finally:
    # 关闭文件 locals()方法会返回当前作用域中的变量集合
    if index_data_file is not None and 'index_data_file' in locals():
        index_data_file.close()
    if value_data_file is not None and 'value_data_file' in locals():
        value_data_file.close()
    if index_value_data_file is not None and 'index_value_data_file' in locals():
        index_value_data_file.close()

print('\n用with处理文件：')
try:
    # 以写模式打开文件（如果文件不存在则会创建），'a'表示追加内容
    with open('index_data.txt', 'a') as index_data_file:
        index_data_file.write(str(index_data))
    with open('value_data.txt', 'a') as value_data_file:
        value_data_file.write(str(value_data))
    with open('index_value_data.txt', 'a') as index_value_data_file:
        index_value_data_file.write(str(index_value_data))
except IOError as e:
    print('Error:' + str(e))

print('\n利用pickle“腌制”数据：')
try:
    # 'b'表示以二进制模式打开数据文件
    with open('index_data.pickle', 'wb') as index_data_file:
        pickle.dump(index_data, index_data_file)
    with open('value_data.pickle', 'wb') as value_data_file:
        pickle.dump(value_data, value_data_file)
    with open('index_value_data.pickle', 'wb') as index_value_data_file:
        pickle.dump(index_value_data, index_value_data_file)

    with open('index_data.pickle', 'rb') as index_data_file:
        index_data = pickle.load(index_data_file)
        print(index_data)
    with open('value_data.pickle', 'rb') as value_data_file:
        value_data = pickle.load(value_data_file)
        print(value_data)
    with open('index_value_data.pickle', 'rb') as index_value_data_file:
        index_value_data = pickle.load(index_value_data_file)
        print(index_value_data)
except IOError as e:
    print('Error:' + str(e))

print('\n5、理解数据：')

print('\n排序的两种方式')
with open('index_data.pickle', 'wb') as index_data_file:
    pickle.dump('2,3,1,10,8,5', index_data_file)
with open('index_data.pickle', 'rb') as index_data_file:
    index_data = pickle.load(index_data_file)
index_data_ = index_data.strip().split(',')
print(index_data_)
index_data_new = sorted(index_data_)
print(index_data_)
print(index_data_new)
index_data_.sort()
print(index_data_)

print('\ndict排序')
dict_sort_test = {
    '2': {'idx': 2, 'name': 'x'},
    '3': {'idx': 3, 'name': 'y'},
    '1': {'idx': 1, 'name': 'z'}
}
# max_idx = max(dict_sort_test.items(), key=lambda xx: xx['idx'])
# print('max_idx', max_idx)
# print(sorted(dict_sort_test.items(), key=lambda xx: xx[0]))
# print(sorted(dict_sort_test.items(), key=lambda xx: xx[1]))
print(dict_sort_test.values())
print(sorted(dict_sort_test.values(), key=lambda xx:xx['idx'], reverse=True))
print(sorted(dict_sort_test.values(),
             key=lambda pro: pro['idx'],
             reverse=True)[0]['idx'])
print(dict_sort_test)
# print(sorted(dict_sort_test, key=dict_sort_test.get))


# 因为是自字符串分割得到的列表，所以是字符串的数字列表，排序可能不同于数字排序，下面将列表转为数字
print('\n将字符串列表转为数字列表后排序：')
with open('index_data.pickle', 'rb') as index_data_file:
    index_data = pickle.load(index_data_file)
index_data_ = [int(each_item) for each_item in index_data.strip().split(',')]
print(index_data_)
# 可以指定reverse=True降序，默认不指定是False升序
index_data_new = sorted(index_data_, reverse=True)
print(index_data_)
print(index_data_new)
index_data_.sort()
print(index_data_)

print('\n推导列表：')
# 分转秒
minutes = [1, 2, 3]
seconds = [m * 60 for m in minutes]
print(seconds)

# 小写转大写
lowers = ['hello', 'world', 'python']
uppers = [word.upper() for word in lowers]
print(uppers)


# 时间格式统一化
def sanitize(time_string):
    if '-' in time_string:
        splitter = '-'
    elif ':' in time_string:
        splitter = ':'
    else:
        return time_string
    (time_prefix, time_suffix) = time_string.split(splitter)
    return time_prefix + '.' + time_suffix


times = ['2-23', '2:21', '2.24']
times_new = sorted(times)
print(times)
print(times_new)
times = [sanitize(time) for time in times]
times_new = sorted(times)
print(times)
print(times_new)

print('\n迭代删除重复项：')
names = ['oyjx', 'ouyangjx', 'ouyangjingxiong', 'oyjx']
unique_names = []
for each_item in names:
    if each_item not in unique_names:
        unique_names.append(each_item)
print(unique_names)

print('\n利用set集合删除重复项')
unique_names_new = set(names)
print(unique_names_new)

# 组合用法
times = ['2.30', '2-23', '2:21', '2.24', '2.21']
print(sorted(set([sanitize(time) for time in times]), reverse=True)[0:3])

print('\n6、定制数据对象：')

print('\n列表与字典：')
# 下面两种方法都可以创建空列表和字典
list_2 = []
list_1 = list()
dict_1 = {}
dict_2 = dict()
print(type(list_1))
print(type(list_2))
print(type(dict_1))
print(type(dict_2))

list_1 = ['oyjx_1', 175, 'oyjx_2', 176]
(name, height) = (list_1.pop(0), list_1.pop(0))
dict_1[name] = height
print(dict_1)

dict_2['name'] = 'oyjx'
dict_2['height'] = [175, 176]
print(dict_2['name'])
print(dict_2['height'][-2])
print(dict_2['height'][0])

dict_3 = {'name': 'oyjx', 'height': [175, 176]}
print(dict_3['name'])
print(dict_3['height'][-1])
print(dict_3['height'][1])

# dict的遍历
for key, value in dict_3.items():
    print('key:', key, ' value:', str(value))

times_data = 'oyjx,2.30,2-23,2:21,2.24,2.21'
times_data_list = times_data.strip().split(',')
times_data_dict = {
    'name': times_data_list.pop(0),
    'times': sorted(set([sanitize(time) for time in times_data_list]), reverse=True)[0:3]
}

print(times_data_dict['name'] + '\'s times is:' + str(times_data_dict['times']))

print('\n定义一个类：')


class Athlete:
    # self是一个非常重要的参数赋值，如果没有这个赋值，Python解释器无法得出方法调用要应用到哪个对象实例
    # 注意，类代码设计为在所有对象实例间共享：方法是共享的，而属性不共享。self参数可以帮助标识要处理那个对象实例的数据
    def __init__(self, the_name='-', the_height=None, the_times_data=None):
        self.name = the_name
        self.height = the_height
        self.times_data_list = []
        if the_times_data is not None:
            self.times_data_list = the_times_data.strip().split(',')
            self.name = self.times_data_list.pop(0)
        # The code to initialize a "Athlete" object.
        print('Athlete init,name = ' + the_name
              + ', height = ' + (str(the_height) if the_height is not None else '-'))
        # self就是创建类对象的实例
        print(self)
        print()

    # 类中定义的所有其他方的第一个参数都必须是self
    def get_name_len(self):
        return len(self.name)

    def get_times(self):
        return sorted(set([sanitize(the_item) for the_item in self.times_data_list]), reverse=True)[0:3]

    def add_time(self, the_time_value):
        self.times_data_list.append(the_time_value)

    def add_times(self, the_time_list):
        self.times_data_list.extend(the_time_list)


# 创建“Athlete”对象，然后赋值给对象，所有这些变量都是唯一的，类型都是Athlete
a = Athlete()
b = Athlete('oyjx', [175, 176])
c = Athlete('ouyang', [177, 178])
d = Athlete('ouyangjx', [179, 174])
print(a)
print(b)
print(c)
print(d)
print(a.get_name_len())
# 在一个对象实例上调用类方法时，Python要求第一个参数是调用对象实例，这往往赋至各方法的self参数
print(Athlete.get_name_len(a))
print(b.get_name_len())
print(c.get_name_len())
print(d.get_name_len())

f = Athlete(the_times_data='oyjx,2.30,2-23,2:21,2.24,2.21')
print(f.name + '\'s times is:' + str(f.get_times()))

a.name = 'oyjx_'
a.add_time('2-45')
a.add_times(['2:36', '2.25', '2-76'])
print(a.name + '\'s times is:' + str(a.get_times()))

print('\nPython继承：')


# 提供一个类名， 新类将派生list类
class NamedList(list):
    def __init__(self, the_name):
        # 初始化派生的类
        list.__init__([])
        self.name = the_name


name_list = NamedList('oyjx')

# name_list是一个“NameList”
print(type(name_list))
# name_list可以做列表能做的所有事情和自己能做的所有事情
print(dir(name_list))

# 追加元素和扩展列表
name_list.append('废柴')
name_list.extend(['傻逼', '白痴'])
print(name_list)

# 遍历
for item in name_list:
    print(name_list.name + 'is a ' + item + '.')

print('\n扩展Athlete成AthleteList：')


class AthleteList(list):
    def __init__(self, the_name='-', the_times_data=None):
        # 初始化派生的类
        list.__init__([])
        self.name = the_name
        if the_times_data is not None:
            self.extend(the_times_data.strip().split(','))
            self.name = self.pop(0)

    def get_name_len(self):
        return len(self.name)

    def get_times(self):
        return sorted(set([sanitize(the_item) for the_item in self]), reverse=True)[0:3]


athlete_list = AthleteList(the_times_data='oyjx,2.30,2-23,2:21,2.24,2.21')
print(athlete_list.name + '\'s times is:' + str(athlete_list))

athlete_list_ = AthleteList(the_name='oyjx_')
athlete_list_.append('2-45')
athlete_list_.extend(['2:36', '2.25', '2-76'])
print(athlete_list_.name + '\'s times is:' + str(athlete_list_.get_times()))

print('\nPython多重继承：')


# # multiple bases have instance lay-out conflict
class AthleteNamedList(Athlete, NamedList):
    def __init__(self, the_name='-'):
        Athlete.__init__(self, the_name=the_name)
        NamedList.__init__(self, the_name=the_name)
        self.name = the_name

    def get_name_len(self):
        return len(self.name)


athlete_named_list = AthleteNamedList(the_name='oyjx')
athlete_named_list.append('oyjx')
print(athlete_named_list.get_times())
print(athlete_named_list)

print('\nlambda & filter：')
for x in filter(lambda y: y % 3 == 0, range(10)):
    print(x)

# 0 3 6 9没有因为结果是0
for x in filter(lambda y: y % 3, range(10)):
    print(x)

print('\nCollection:')
list_ = list(range(20))
index_ = [0]
for i in index_:
    list_[i] = None
print(list_)

list_ = [1, 2, None]
# @Todo
print(list(filter(lambda the_index: item is not None, enumerate(list_))))

# @Todo 能否返回下标？
print([(lambda the_item: the_item is not None)(item) for index, item in enumerate(list_)])

new_list_ = [i if list_[i] is not None else -1 for i in range(len(list_))]
new_list_ = list(filter(lambda the_item: the_item != -1, iter(new_list_)))
print(new_list_)

list_ = []
if list_:
    print('list_有元素')

if not list_:
    print('空list_')

test_dict = {1: 3}
print(len(test_dict))
test_dict.pop(1)
print(test_dict)

print('\nNumber:')
print(0 % 45)
a = '0.5'
a = 60 * float(a)
print(a)

print('\nround:')
print(round(25.25 - 25.24, 2))
print(round(25.25 - 0.01, 2))

print('\nceil:')
print(math.ceil(1 / 5))
print(math.ceil(0.21323 * 60))
print(0.21323 * 60)

print('\nNone:')
print(str(None))
