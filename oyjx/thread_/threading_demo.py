import sys
import threading
import time
import queue
import random
import re
from concurrent.futures import ThreadPoolExecutor
from urllib import request

sys.path.append("..")
from common.common_test import *

"""
参考：
    https://www.cnblogs.com/wang-can/p/3580457.html
    《Python 核心编程》
    ...
    
目录：
    1、创建线程
        Python3的两种的方法
    2、Timer定时器
    3、简单锁实现同步
        threading的不可重入锁（threading.Lock()）和可重入锁（threading.RLock()）
    4、Condition条件变量
    5、Semaphore同步
    6、Event
    7、local线程局部存储
    8、Queue
    9、Barrier
    10、concurrent.future
    ...
    
特殊用法：
    Python 2.5或更新版本，有只用方法可以不再调用锁的acquire()和release()方法，从而进一步简化代码
    这就是使用with语句，此时每个对象的上下文管理器负责在该套件之前调用acquire()并在完成执行之后调用release()
    threading模块的对象Lock、RLock、Condition、Semaphore、BoundSemaphore都包含上下文管理器，都可以使用with语句
    
关于多线程：
    GIL（全局解释器锁）
    I/O密集型应用和计算密集型应用
    ...
"""

# 可以指定1-x执行哪些程序，或者指定为[0]执行全部
exe_list = [0]

print('1、线程：')
'''
Python中有两个线程模块，分别是thread和threading，threading是thread的升级版。threading的功能更强大。
创建线程有3种方法：
　　　　1、thread模块的start_new_thread函数
　　　　2、继承自threading.Thread模块
　　　　3、用threading.Thread直接返回一个thread对象，然后运行它的start方法
'''


def func(the_nums):
    for num_item in the_nums:
        # 可以用threadTest，说明可以引用运行时变量？
        # 也可以使用threading.currentThread()
        print('current thread:' + threadTest.getName() + ' num:' + repr(num_item))
        print(threading.current_thread())


def func_(a):
    print('废柴' + a)


# 线程
print('\n1.1、线程（用threading.Thread直接返回一个thread对象）：')
if is_exec_curr(exe_list, 1) and __name__ == '__main__':
    nums = list(range(100))
    print(nums[80: 1 * 100])
    for i in range(5):
        # range(5) => 0 1 2 3 4
        # [0: 20] [20: 40] [40: 60] [60: 80] [80: 100]
        threadTest = threading.Thread(target=func, args=(nums[i * 20: (i + 1) * 20],))  # ,不能少
        # func_() argument after * must be an iterable, not int
        # threadTest = threading.Thread(target=func_, args='啊',)
        threadTest.start()

    print('active count:' + str(threading.active_count()))
    time.sleep(2)
    # MainThread并非是守护线程
    print('active count:' + str(threading.active_count()) + ' current thread:'
          + str(threading.current_thread()) + ' is daemon:'
          + str(threading.current_thread().isDaemon()))

print('\n1.2、线程（thread模块的start_new_thread函数）：')
if is_exec_curr(exe_list, 1) and __name__ == '__main__':
    # Python好像没有默认的thread类库了
    print('Python3没有')

print('\n1.3、线程（继承自threading.Thread模块）：')


class MyThread(threading.Thread):

    def __init__(self, the_id, interval):
        threading.Thread.__init__(self)

        self.id = the_id
        self.interval = interval

    # 必须重写run函数，而且想要运行应该调用start方法
    def run(self):
        # 遍历[0 - 10) 之间能 % interval等于0的，也就是能被interval整除的数
        for x in filter(lambda x: x % self.interval == 0, range(10)):
            print('Thread is:%d time is %d' % (self.id, x))


if is_exec_curr(exe_list, 1) and __name__ == '__main__':
    t1 = MyThread(1, 2)
    t2 = MyThread(2, 4)

    t1.start()
    t2.start()

    # t1、t2调用join是等待t1、t2线程都执行完，且join()方法可以指定超时时间
    t1.join()
    t2.join()

print('\n2、定时器：')


def hello_world(name):
    print(name + ",hello world!")

    # @Todo 好不好看，有没有其它方式
    # Timer：隔一定时间调用一个函数，如果想实现每隔一段时间就调用一个函数的话，就要在Timer调用的函数中，再次设置Timer
    # Timer是Thread的一个派生类
    global timer
    timer = threading.Timer(2.0, hello_world, [languages[random.randint(0, len(languages) - 1)]])
    timer.start()


if is_exec_curr(exe_list, 2) and __name__ == "__main__":
    languages = ['Java', 'Python', 'C', 'C++', 'R', 'Ruby']
    timer = threading.Timer(2.0, hello_world, [languages[random.randint(0, len(languages) - 1)]])
    timer.start()
    time.sleep(4)
    # 取消定时器
    timer.cancel()

print('\n3、简单锁实现同步：')

print('\n3.1、不可重入锁：')


def count(the_id):
    global num

    while True:
        try:
            lock.acquire()

            if num <= 10:
                print('Thread is:%s and the num is %s' % (the_id, num))
                num += 1
            else:
                break

        finally:
            # 保证锁释放必须执行（如果不放在finally块中，可能直接break了没有释放锁）
            lock.release()


if is_exec_curr(exe_list, 3) and __name__ == "__main__":
    lock = threading.Lock()

    num = 1
    t1 = threading.Thread(target=count, args=('A',))
    t2 = threading.Thread(target=count, args=('B',))

    t1.start()
    t2.start()

    time.sleep(2)

print('\n3.2、可重入锁：')


def count_(the_id):
    global num_

    """
    可以用“with lock_:”替换
        try:
            lock_.acquire()
        finally:
            lock_.release()
    """

    with lock_:
        # try:
        # 在这个递归方法里面必须用可重入锁，否则会死锁
        # lock_.acquire()

        if num_ <= 10:
            print('Thread is:%s and the num is %s' % (the_id, num_))
            num_ += 1
            count_(the_id)
    # finally:
    # lock_.release()


if is_exec_curr(exe_list, 3) and __name__ == "__main__":
    lock_ = threading.RLock()

    num_ = 1
    t3 = threading.Thread(target=count_, args=('C',))
    t4 = threading.Thread(target=count_, args=('D',))

    t3.start()
    t4.start()

    time.sleep(2)

print('\n4、Condition条件变量：')


class Buf:

    def __init__(self):
        self.condition = threading.Condition()
        self.data = []

    def __is_empty(self):
        return len(self.data) == 0

    def __is_full(self):
        return len(self.data) == LIST_MAX_ELEMENT

    def get(self):
        """

        可以用“with self.condition:”替换
            try:
                self.condition.acquire()
            finally:
                self.condition.release()
        """
        with self.condition:
            # try:
            # self.condition.acquire()

            while self.__is_empty():
                self.condition.wait()

            temp = self.data.pop(0)

            """
            移除了元素通知在调用put()方法的线程
            唤醒一个线程就行了，因为只会取出一个，可以不用notify_all()
            """
            self.condition.notify()
            return temp
        # finally:
        #     self.condition.release()

    def put(self, put_info):
        """

        :param put_info:放如集合的数据
        :return:
        """
        try:
            self.condition.acquire()

            while self.__is_full():
                self.condition.wait()

            self.data.append(put_info)

            """
            有新的元素通知在调用get()方法的线程
            唤醒一个线程就行了，因为只会放入一个，可以不用notify_all()
            """
            self.condition.notify_all()
        finally:
            self.condition.release()


def product(the_id, the_num):
    for item in range(the_num):
        info.put(item + 1)
        print('product%s %s\n' % (the_id, str(item + 1)))


def customer(the_id, the_num):
    for item in range(the_num):
        temp = info.get()
        print('customer%s %s\n' % (the_id, str(temp)))


if is_exec_curr(exe_list, 4) and __name__ == "__main__":
    # 限制列表最多可以防止的元素
    LIST_MAX_ELEMENT = 5

    info = Buf()

    p = threading.Thread(target=product, args=('P', 10))
    c1 = threading.Thread(target=customer, args=('C1', 5))
    c2 = threading.Thread(target=customer, args=('C2', 5))

    p.start()
    time.sleep(1)
    c1.start()
    c2.start()

    p.join()
    c1.join()
    c2.join()

print('\n5、Semaphore同步：')
"""
Semaphore，是一种带计数的线程同步机制，当调用release时，增加计算，当acquire时，减少计数，当计数为0时，自动阻塞，等待release被调用。

而在Python中存在两种Semaphore，一种就是纯粹的Semaphore，还有一种就是BoundedSemaphore，区别：
Semaphore：在调用release()函数时，不会检查，增加的计数是否超过上限（没有上限，会一直上升）
BoundedSemaphore：在调用release()函数时，会检查，增加的计数是否超过上限，这样就保证了使用的计数
"""


def semaphore_test():
    print('Thread %s is waiting Semaphore' % threading.currentThread().getName())

    """
    可以用“with semaphore:”替换
        try:
            semaphore.acquire()
        finally:
            semaphore.release()
    """

    with semaphore:
        # try:
        # 获取资源，计数 - 1
        # semaphore.acquire()
        print('Thread %s get Semaphore' % threading.currentThread().getName())
        time.sleep(1)
        print('Thread %s release Semaphore' % threading.currentThread().getName())
    # finally:
    # 释放资源，计数 + 1
    # semaphore.release()


if is_exec_curr(exe_list, 5) and __name__ == "__main__":
    semaphore = threading.Semaphore(3)
    # semaphore = threading.BoundedSemaphore(3)

    t1 = threading.Thread(target=semaphore_test)
    t2 = threading.Thread(target=semaphore_test)
    t3 = threading.Thread(target=semaphore_test)
    t4 = threading.Thread(target=semaphore_test)

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

    # 这里因为是简单的Semaphore，哪怕计数已满，也可以再次释放，不会报错，而BoundedSemaphore，则会报错。
    semaphore.release()

print('\n6、Event：')
"""
Event:  是线程同步的一种方式，类似于一个标志，当该标志为false时，所有等待该标志的线程阻塞，当为true时，所有等待该标志的线程被唤醒
isSet():  　　　　 当内置标志为True时返回True。 
set():     　　　　将标志设为True，并通知所有处于等待阻塞状态的线程恢复运行状态。 
clear():   　　　　将标志设为False。 
wait([timeout]):  如果标志为True将立即返回，否则阻塞线程至其他线程调用set()。

有点类似于Java的CountDownLatch，但不太一样，可以反过来用，比如某个线程完成之后，其他线程才可以开始
"""


def event_test():
    print('Thread %s is waiting event' % threading.currentThread().getName())
    event.wait()
    print('Thread %s get the event' % threading.currentThread().getName())


if is_exec_curr(exe_list, 6) and __name__ == "__main__":
    event = threading.Event()

    t1 = threading.Thread(target=event_test)
    t2 = threading.Thread(target=event_test)

    t1.start()
    t2.start()

    time.sleep(2)

    print('isSet:' + str(event.is_set()))
    print('Main thread set event')
    event.set()
    print('isSet:' + str(event.is_set()))

    t1.join()
    t2.join()

print('\n7、local线程局部存储：')
"""
线程局部存储（tls），对于同一个local，线程无法访问其他线程设置的属性；线程设置的属性不会被其他线程设置的同名属性替换。

"""


def local_test(value):
    local.name = value
    print('local name:' + local.name)


if is_exec_curr(exe_list, 7) and __name__ == "__main__":
    local = threading.local()
    local.name = 'main'

    t1 = threading.Thread(target=local_test, args=('localA',))
    t2 = threading.Thread(target=local_test, args=('localB',))

    t1.start()
    t1.join()

    t2.start()
    t2.join()

    print('local name:' + local.name)

print('\n8、Queue：')
"""
Queue(maxsize=0)  # 创建一个先入先出队列，如果给定最大值，则在队列没有空间时阻塞，否则为无限队列
LifoQueue(maxsize=0)  # 创建一个先入后出队列，……
PriorityQueue(maxsize=0)  # 创建一个优先级队列，……
对象方法：
qsize()  # 返回队列大小（由于返回时队列打下可能被其他线程修改，所以该值为近似值）
empty()  # 如果队列为空，返回True
full()  # 如果队列已满，返回True
put(item, block=True, timeout=None)  # 将item放入队列，如果block为True，则在有可用空间之前且超时之前一致阻塞
put_nowait(item)  # 和put(item, False)相同
get(block=True, timeout=None)  # 从队列中得到元素，如果block为True，则有可用元素之前且超时之前一直阻塞
get_nowait()  # 和get(False)相同
task_done()  # 用于队列中某个元素已执行完成，该方法会被下面的join()使用
join()  # 在队列中所有元素执行完毕并调用上面的task_done()信号之前，保持阻塞
"""


class MyThread(threading.Thread):
    def __init__(self, the_func, the_args, the_name=''):
        threading.Thread.__init__(self)
        self.name = the_name
        self.func = the_func
        self.args = the_args

    def run(self):
        self.func(*self.args)


def write_queue(the_queue):
    print('producing object for queue')
    the_queue.put('xxx', True)
    print('size now:', the_queue.qsize())


def read_queue(the_queue):
    the_queue.get(True)
    print('consumed object form queue,size now:', the_queue.qsize())


def writer(the_queue, loops):
    for item in range(loops):
        write_queue(the_queue)
        time.sleep(random.randint(1, 2))


def reader(the_queue, loops):
    for item in range(loops):
        read_queue(the_queue)
        time.sleep(random.randint(3, 5))


if is_exec_curr(exe_list, 8) and __name__ == "__main__":
    funcs = [writer, reader]
    funcs_num = range(len(funcs))
    loops_num = random.randint(2, 5)
    queue = queue.Queue(45)
    threads = []
    for i in funcs_num:
        t = MyThread(funcs[i], (queue, loops_num), funcs[i].__name__)
        threads.append(t)

    for i in funcs_num:
        threads[i].start()

    for i in funcs_num:
        threads[i].join()

    print('all done.')

print('\n9、Barrier：')


def referee():
    total_step = 20
    if step1 >= total_step or total_step > 100:
        print('A win' if step1 > step2 else 'B win')
        # barrier.abort()
        # 可以选择抛出异常，然后会看源码（_release()）是会调用_break()，修改_state，唤醒所有wait()的线程
        # wait()的线程再次运行再次调用wait()时，每次wait()都会先调用_enter()检测到状态
        # 发现_state = -2 < 0，则抛出BrokenBarrierError异常
        # 至于为什么不能调用abort()方法？
        # 因为abort()有这段代码：“with self._cond:”，当前已经持有Condition对象，不能再次持有
        # @Todo 上面的原因待证实（应该就是这个）
        raise threading.BrokenBarrierError
    else:
        print()
        time.sleep(0.5)


def test1(name):
    global step1

    try:
        while True:
            step1 += random.randint(4, 5)
            print('*' * step1 + name)
            barrier.wait()
    except threading.BrokenBarrierError:
        print(name + ' broken')


def test2(name):
    global step2

    try:
        while True:
            step2 += random.randint(4, 5)
            print('*' * step2 + name)
            barrier.wait()
    except threading.BrokenBarrierError:
        print(name + ' broken')


def test3(name):
    try:
        barrier.wait()
    except threading.BrokenBarrierError:
        print(name + ' broken')


def test4(name):
    try:
        barrier.wait()
    except threading.BrokenBarrierError:
        print(name + ' broken')


def test5(name):
    try:
        barrier.wait()
    except threading.BrokenBarrierError:
        print(name + ' broken')


if is_exec_curr(exe_list, 9) and __name__ == "__main__":
    count = 0
    step1 = 0
    step2 = 0
    barrier = threading.Barrier(2, action=referee)

    test1 = MyThread(test1, ('A',), 'test1')
    test1.start()
    test2 = MyThread(test2, ('B',), 'test2')
    test2.start()

    test1.join()
    test2.join()

    print(barrier.n_waiting)  # 0
    print(barrier.broken)  # True
    print(barrier._state)  # -2
    print(barrier._count)  # 0
    print()

    barrier.reset()

    print(barrier.n_waiting)  # 0
    print(barrier.broken)  # False
    print(barrier._state)  # 0
    print(barrier._count)  # 0
    print()

    test3 = MyThread(test3, ('C',), 'test3')
    test3.start()

    print(barrier.n_waiting)  # 1
    print(barrier.broken)  # False
    print(barrier._state)  # 0
    print(barrier._count)  # 1
    print()

    # barrier.abort()
    barrier.reset()
    time.sleep(0.5)
    # 执行 abort 或者 reset 的结果：
    # 虽然执行reset，_state先会变-1，但阻塞的线程会被唤醒，finally块会执行_exit，最终_state还是变回0
    print(barrier.n_waiting)  # 0 / 0
    print(barrier.broken)  # True / False
    print(barrier._state)  # -2 / 0
    print(barrier._count)  # 0 / 0
    print()

    # test4 = MyThread(test4, ('D',), 'test4')
    # test4.start()
    #
    # test5 = MyThread(test5, ('E',), 'test5')
    # test5.start()

print('\n10、concurrent.future：')
pattern = re.compile('#([\d,]+) in Books ')
amazon_url = 'https://amazon.com/dp/'
isbn_data = {
    '0132269937': 'Core Python Programming',
    '0132356139': 'Python Web Development with Django',
    '0137143419': 'Python Fundamentals',
}


def get_ranking(the_isbn):
    url = '%s%s' % (amazon_url, the_isbn)
    print(url)
    # 设置下请求头之类的吧，实在抓不到看下是否还需要cookie https://amazon.com/dp/0132269937
    response = request.urlopen(url)
    data = response.read().decode('utf-8')
    print(str(data) + ' -')
    print('-')
    return str(pattern.findall(data)[0], 'utf-8')


def show_ranking(the_isbn):
    print('- %r ranked %s' % (isbn_data[the_isbn], get_ranking(the_isbn)))


if is_exec_curr(exe_list, 10) and __name__ == "__main__":
    print('1.At', time.ctime(), 'on Amazon')
    # 异常好像被吃掉了= = @Todo
    with ThreadPoolExecutor(3) as executor:
        for isbn in isbn_data:
            executor.submit(show_ranking, isbn)
    print('1.all done at:', time.ctime())

    print('2.At', time.ctime(), 'on Amazon')
    with ThreadPoolExecutor(3) as executor:
        for isbn, ranking in zip(isbn_data, executor.map(get_ranking, isbn_data)):
            print('- %r ranked %s' % (isbn_data[isbn], ranking(isbn)))
    print('2.all done at:', time.ctime())
