# procs-python-threading.md
⊕ [Combining Coroutines with Threads and Processes — PyMOTW 3](https://pymotw.com/3/asyncio/executors.html)
    A ThreadPoolExecutor starts its worker threads and then calls each of the provided functions once in a thread. This example shows how to combine run_in_executor() and wait() to have a coroutine yield control to the event loop while blocking functions run in separate threads, and then wake back up when those functions are finished.
    A ProcessPoolExecutor works in much the same way, creating a set of worker processes instead of threads. Using separate processes requires more system resources, but for computationally-intensive operations it can make sense to run a separate task on each CPU core.

⊕ [ThreadLocal - 廖雪峰的官方网站](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431928972981094a382e5584413fa040b46d46cce48e000)
    # 创建全局ThreadLocal对象: local_school = threading.local()
    全局变量local_school就是一个ThreadLocal对象，每个Thread对它都可以读写student属性，但互不影响。你可以把local_school看成全局变量，但每个属性如local_school.student都是线程的局部变量，可以任意读写而互不干扰，也不用管理锁的问题，ThreadLocal内部会处理。
    可以理解为全局变量local_school是一个dict，不但可以用local_school.student，还可以绑定其他变量，如local_school.teacher等等。

    ThreadLocal最常用的地方就是为每个线程绑定一个数据库连接，HTTP请求，用户身份信息等，这样一个线程的所有调用到的处理函数都可以非常方便地访问这些资源。

```python
import threading

# 创建全局ThreadLocal对象:
local_school = threading.local()

def process_student():
    # 获取当前线程关联的student:
    std = local_school.student
    print('Hello, %s (in %s)' % (std, threading.current_thread().name))

def process_thread(name):
    # 绑定ThreadLocal的student:
    local_school.student = name
    process_student()

t1 = threading.Thread(target= process_thread, args=('Alice',), name='Thread-A')
t2 = threading.Thread(target= process_thread, args=('Bob',), name='Thread-B')
t1.start()
t2.start()
t1.join()
t2.join()
```

    