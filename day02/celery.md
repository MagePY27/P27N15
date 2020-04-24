### celery 组件
> 参考文档： https://www.celerycn.io
- worker （任务执行者），用来执行具体任务，可在多台服务器部署实现扩展，项目中我们使用 python 进行开发
- broker （中间人），用来实现任务调度、worker 管理等功能；支持 RabbitMQ、Redis、Zookeeper 等中间件，项目中使用redis
- backend 用来存储任务结果，项目中我们使用 redis
- application （应用），用来实例化 celery
- tasks （任务），用来构建 application

#### celery task
- 针对任务执行的过程的各个状态进行特殊处理
```python
from celery import Task


class MyTask(Task):
    abstract = True

    # 任务返回结果后执行
    def after_return(self, *args, **kwargs):
        print('任务返回结果: {0!r}'.format(self.request))

    # 任务执行失败是调用
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('任务执行失败!', exc)

    # 任务重试时调用
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        print('任务正在重试')

    # 任务成功时调用
    def on_success(self, retval, task_id, args, kwargs):
        print('任务执行成功')

```

- celery 任务
```python
# 最简化构建一个 celery 应用，指定了 broker 和 backend
from celery import Celery
from ops2.utils.MyTask import MyTask

# 定义 broker 和 backend，分别为任务中间人和结果保存路径
BROKER = "redis://:@127.0.0.1:6379/3"
BACKEND = "redis://:@127.0.0.1:6379/4"

app = Celery("tasks", broker=BROKER, backend=BACKEND, )
# 添加event
app.conf.task_send_sent_event = True
app.conf.worker_send_task_events = True
# 在 app 初始化完毕，进行 app 时区项配置
app.conf.CELERY_TIMEZONE = 'Asia/Shanghai'
app.conf.timezone = 'Asia/Shanghai'


# 定义一个任务，名字为 add
@app.task(bind=True, max_retries=3)
def add(self, x, y):
    try:
        c = x + y
        print('计算结果为： %d ' % c)
        return c
    except Exception as e:
        raise self.retry(exc=e, countdown=1)
'''
retry的参数可以有：
                    exc：指定抛出的异常
                    throw：重试时是否通知worker是重试任务
                    eta：指定重试的时间／日期
                    countdown：在多久之后重试（每多少秒重试一次）
                    max_retries：最大重试次数
'''
```

- 执行任务脚本
```python
# 脚本用来发送 celery 任务
# 最基本推送一个任务，不支持任何选项
ret = add.delay(3, 6)
print(ret.get())
# 错误的输入，触发重试
add.delay(3, 'aaa')
```

- 运行celery
> -A; 指定使用的 app

> -l; 指定日志级别

> -f; 指定日志文件

> -D; 后台运行

> --pidfile； 指定 pid 文件路径

> -c； 启动子进程个数，默认为 cpu 核数

> worker; 启动 worker

```text
(ops-py3venv) [ops@ops-3 ops2]$ celery -A test_celery worker -l info -n aa
 
 -------------- celery@aa v4.3.0 (rhubarb)
---- **** ----- 
--- * ***  * -- Linux-3.10.0-957.el7.x86_64-x86_64-with-centos-7.6.1810-Core 2020-04-24 14:32:47
-- * - **** --- 
- ** ---------- [config]
- ** ---------- .> app:         tasks:0x7fb6ac945588
- ** ---------- .> transport:   redis://127.0.0.1:6379/3
- ** ---------- .> results:     redis://127.0.0.1:6379/4
- *** --- * --- .> concurrency: 4 (prefork)
-- ******* ---- .> task events: ON
--- ***** ----- 
 -------------- [queues]
                .> celery           exchange=celery(direct) key=celery
                

[tasks]
  . task-add

[2020-04-24 14:32:47,969: INFO/MainProcess] Connected to redis://127.0.0.1:6379/3
[2020-04-24 14:32:47,976: INFO/MainProcess] mingle: searching for neighbors
[2020-04-24 14:32:48,993: INFO/MainProcess] mingle: all alone
[2020-04-24 14:32:49,009: INFO/MainProcess] celery@aa ready.


```
- 执行脚本
```text
(ops-py3venv) [ops@ops-3 ops2]$ python test_sender.py 
9
```

- 返回结果
```text
[2020-04-24 14:33:24,919: INFO/MainProcess] Received task: task-add[86aa5104-bd5f-4f69-9b83-00d326b33ffe]  
[2020-04-24 14:33:24,921: WARNING/ForkPoolWorker-1] 计算结果为： 9
[2020-04-24 14:33:24,927: WARNING/ForkPoolWorker-1] 任务执行成功
[2020-04-24 14:33:24,927: INFO/ForkPoolWorker-1] Task task-add[86aa5104-bd5f-4f69-9b83-00d326b33ffe] succeeded in 0.005902154998693732s: 9
[2020-04-24 14:33:24,927: WARNING/ForkPoolWorker-1] 任务返回结果: <Context: {'lang': 'py', 'task': 'task-add', 'id': '86aa5104-bd5f-4f69-9b83-00d326b33ffe',
 'shadow': None, 'eta': None, 'expires': None, 'group': None, 'retries': 0, 'timelimit': [None, None], 'root_id': '86aa5104-bd5f-4f69-9b83-00d326b33ffe', 'parent_id': None, 'argsrepr': '(3, 6)', 'kwargsrepr': '{}', 'origin': 'gen13070@ops-3', 'reply_to': '15cddccf-c46c-33dc-b2f0-e337e1a57591', 'correlation_id': '86aa5104-bd5f-4f69-9b83-00d326b33ffe', 'delivery_info': {'exchange': '', 'routing_key': 'celery', 'priority': 0, 'redelivered': None}, 'args': [3, 6], 'kwargs': {}, 'hostname': 'celery@aa', 'is_eager': False, 'callbacks': None, 'errbacks': None, 'chain': None, 'chord': None, 'called_directly': False, '_protected': 1, '_children': []}>[2020-04-24 14:33:24,931: INFO/MainProcess] Received task: task-add[14163e39-a188-424d-b5f8-cb591ed10a31]  
[2020-04-24 14:33:24,975: INFO/MainProcess] Received task: task-add[14163e39-a188-424d-b5f8-cb591ed10a31]  ETA:[2020-04-25 02:33:25.933980+08:00] 
[2020-04-24 14:33:24,979: WARNING/ForkPoolWorker-2] 任务正在重试
[2020-04-24 14:33:24,979: INFO/ForkPoolWorker-2] Task task-add[14163e39-a188-424d-b5f8-cb591ed10a31] retry: Retry in 1s: TypeError("unsupported operand type
(s) for +: 'int' and 'str'",)[2020-04-24 14:33:26,254: INFO/MainProcess] Received task: task-add[14163e39-a188-424d-b5f8-cb591ed10a31]  ETA:[2020-04-25 02:33:27.183343+08:00] 
[2020-04-24 14:33:26,257: WARNING/ForkPoolWorker-1] 任务正在重试
[2020-04-24 14:33:26,257: INFO/ForkPoolWorker-1] Task task-add[14163e39-a188-424d-b5f8-cb591ed10a31] retry: Retry in 1s: TypeError("unsupported operand type
(s) for +: 'int' and 'str'",)[2020-04-24 14:33:27,494: INFO/MainProcess] Received task: task-add[14163e39-a188-424d-b5f8-cb591ed10a31]  ETA:[2020-04-25 02:33:28.493052+08:00] 
[2020-04-24 14:33:27,495: WARNING/ForkPoolWorker-2] 任务正在重试
[2020-04-24 14:33:27,495: INFO/ForkPoolWorker-2] Task task-add[14163e39-a188-424d-b5f8-cb591ed10a31] retry: Retry in 1s: TypeError("unsupported operand type
(s) for +: 'int' and 'str'",)[2020-04-24 14:33:28,502: WARNING/ForkPoolWorker-1] 任务执行失败!
[2020-04-24 14:33:28,502: WARNING/ForkPoolWorker-1] unsupported operand type(s) for +: 'int' and 'str'
[2020-04-24 14:33:28,502: ERROR/ForkPoolWorker-1] Task task-add[14163e39-a188-424d-b5f8-cb591ed10a31] raised unexpected: TypeError("unsupported operand type
(s) for +: 'int' and 'str'",)Traceback (most recent call last):
  File "/home/ops/ops-py3venv/lib/python3.6/site-packages/celery/app/trace.py", line 385, in trace_task
    R = retval = fun(*args, **kwargs)
  File "/home/ops/ops-py3venv/lib/python3.6/site-packages/celery/app/trace.py", line 648, in __protected_call__
    return self.run(*args, **kwargs)
  File "/home/ops/ops-code/ops2/test_celery.py", line 29, in add
    raise self.retry(exc=e, countdown=1)
  File "/home/ops/ops-py3venv/lib/python3.6/site-packages/celery/app/task.py", line 703, in retry
    raise_with_context(exc)
  File "/home/ops/ops-code/ops2/test_celery.py", line 25, in add
    c = x + y
TypeError: unsupported operand type(s) for +: 'int' and 'str'

```
- 其他调用方式
```text
# 推送一个任务，第一个参数 (2,5) 为任务参数，必须为 tuple 或 list，
# 如果任务只需要一个参数，必须添加逗号进行转换，格式 (var1,)
# countdown=10，10 秒后开始执行
add.apply_async((2, 5), countdown=10)
# 参数的其他写法，
add.apply_async(kwargs={'x': 4, 'y': 8})
add.s(5, 6).apply_async()

# 任务组
from celery import group
numbers = [(2, 2), (4, 4), (8, 8), (16, 16)]
res = group(add.subtask(i) for i in numbers).apply_async()
print(res.get())

# 使用 link，将任务结果作为第一个参数传递到下一个任务
add.apply_async((2, 3), link=add.s(16))

# 同样，前一个任务结果作为下一个任务的第一个参数
from celery import chain
res = chain(add.s(2, 2), add.s(4), add.s(8))()
print(res.get())

# 使用管道符
(add.s(2, 2) | add.s(4) | add.s(8))().get()
```

- 执行效果
```text
(ops-py3venv) [ops@ops-3 ops2]$ python test_sender.py 
9
[4, 8, 16, 32]
16

```

####  进程报警 celery Event
- 添加 test_event.py
```python
from celery import Celery
import json
import time
from test_celery import app


def my_monitor(app):
    state = app.events.State()

    # 处理事件
    def announce_failed_tasks(event):
        state.event(event)
        # task name 仅与-received 事件一起发送，这里我们使用 state 跟踪该事件。
        task = state.tasks.get(event['uuid'])

        print('任务失败: %s[%s] %s' % (
            task.name, task.uuid, task.info(),))

    # 处理事件
    def announce_tasks_callback(event):
        print('任务状态：%s - %s - %s - %s' %
              (event.get('hostname'), event.get('type'), event.get('uuid'),
               time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(event.get('timestamp')))))

    # 处理 worker 事件
    def announce_worker(event):
        if event.get('type') == 'worker-heartbeat':
            print('心跳检测')
        elif event.get('type') == 'worker-offline':
            print('worker 下线：%s - %s - %s ' %
                  (event.get('hostname'), event.get('type'),
                   time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(event.get('timestamp')))))
        elif event.get('type') == 'worker-online':
            print('worker 上线：%s - %s - %s ' %
                  (event.get('hostname'), event.get('type'),
                   time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(event.get('timestamp')))))
        else:
            pass

    with app.connection() as connection:
        recv = app.events.Receiver(connection, handlers={
            # 将 task 事件交给对应的处理函数
            'task-failed': announce_failed_tasks,
            'task-succeeded': announce_tasks_callback,
            'task-received': announce_tasks_callback,
            'task-revoked': announce_tasks_callback,
            'task-retried': announce_tasks_callback,

            # 将 worker 事件交给对应的处理函数
            'worker-online': announce_worker,
            'worker-offline': announce_worker,
        })
        recv.capture(limit=None, timeout=None, wakeup=True)


if __name__ == '__main__':
    my_monitor(app)

```
- 新开shell, 重启celery 效果如下：
```text
(ops-py3venv) [ops@ops-3 ops2]$ python test_event.py 
worker 下线：celery@aa - worker-offline - 2020-04-24 14:38:28 
worker 上线：celery@aa - worker-online - 2020-04-24 14:38:41 
任务状态：celery@aa - task-received - ee7b04a4-0e24-4b73-8528-91792476a4e2 - 2020-04-24 14:39:27
任务状态：celery@aa - task-succeeded - ee7b04a4-0e24-4b73-8528-91792476a4e2 - 2020-04-24 14:39:27
任务状态：celery@aa - task-received - d0ea2fd8-2b63-41bf-9c59-b7207e55bc7b - 2020-04-24 14:39:27
任务状态：celery@aa - task-received - c12dabe9-a927-463f-afc9-7a991fef73f7 - 2020-04-24 14:39:27
任务状态：celery@aa - task-received - f3a0b3ef-15dd-4618-9c7f-c8c4f91ecb2f - 2020-04-24 14:39:27
任务状态：celery@aa - task-received - 701dd90b-5384-4494-8bbd-18474080fc00 - 2020-04-24 14:39:27
任务状态：celery@aa - task-received - 4ac7263f-b583-4698-bb76-f635f5e6ae63 - 2020-04-24 14:39:27
任务状态：celery@aa - task-received - 7c1702b1-5985-4658-b884-e15d05d63e82 - 2020-04-24 14:39:27
任务状态：celery@aa - task-succeeded - f3a0b3ef-15dd-4618-9c7f-c8c4f91ecb2f - 2020-04-24 14:39:27
任务状态：celery@aa - task-succeeded - 701dd90b-5384-4494-8bbd-18474080fc00 - 2020-04-24 14:39:27
任务状态：celery@aa - task-received - 4a3d3f38-a3e6-4bf7-817d-3fabe88d39b8 - 2020-04-24 14:39:27
任务状态：celery@aa - task-received - 7715cb7b-284a-4574-997b-d358bb12e9a1 - 2020-04-24 14:39:27
任务状态：celery@aa - task-succeeded - 4ac7263f-b583-4698-bb76-f635f5e6ae63 - 2020-04-24 14:39:27
任务状态：celery@aa - task-succeeded - 7c1702b1-5985-4658-b884-e15d05d63e82 - 2020-04-24 14:39:27
任务状态：celery@aa - task-succeeded - 4a3d3f38-a3e6-4bf7-817d-3fabe88d39b8 - 2020-04-24 14:39:27
任务状态：celery@aa - task-received - d0ea2fd8-2b63-41bf-9c59-b7207e55bc7b - 2020-04-24 14:39:27
任务状态：celery@aa - task-succeeded - 7715cb7b-284a-4574-997b-d358bb12e9a1 - 2020-04-24 14:39:27
任务状态：celery@aa - task-retried - d0ea2fd8-2b63-41bf-9c59-b7207e55bc7b - 2020-04-24 14:39:27
任务状态：celery@aa - task-received - e1e8d62f-5b09-4127-96e3-e03093eb16a3 - 2020-04-24 14:39:27
任务状态：celery@aa - task-received - 3af69e50-9b1d-48f4-884b-39d4d78331d3 - 2020-04-24 14:39:27
任务状态：celery@aa - task-received - 98c51cdd-338c-4efe-b9ec-c5a2502c4647 - 2020-04-24 14:39:27
任务状态：celery@aa - task-succeeded - 3af69e50-9b1d-48f4-884b-39d4d78331d3 - 2020-04-24 14:39:27
任务状态：celery@aa - task-received - c7796795-510d-4ee4-918a-fafcfc83e1df - 2020-04-24 14:39:27
任务状态：celery@aa - task-succeeded - e1e8d62f-5b09-4127-96e3-e03093eb16a3 - 2020-04-24 14:39:27
任务状态：celery@aa - task-succeeded - c7796795-510d-4ee4-918a-fafcfc83e1df - 2020-04-24 14:39:27
任务状态：celery@aa - task-received - ea89d2ae-d600-4999-9595-afb3f976dac4 - 2020-04-24 14:39:27
任务状态：celery@aa - task-succeeded - 98c51cdd-338c-4efe-b9ec-c5a2502c4647 - 2020-04-24 14:39:27
任务状态：celery@aa - task-succeeded - ea89d2ae-d600-4999-9595-afb3f976dac4 - 2020-04-24 14:39:27
任务状态：celery@aa - task-received - 338d7db6-6ab7-4488-9d64-ea8841001f78 - 2020-04-24 14:39:27
任务状态：celery@aa - task-received - fc5d15ac-c1bc-4ca4-8f1b-3bf8d2415923 - 2020-04-24 14:39:27
任务状态：celery@aa - task-succeeded - 338d7db6-6ab7-4488-9d64-ea8841001f78 - 2020-04-24 14:39:27
任务状态：celery@aa - task-received - ea2e1d39-1e2a-455f-9de8-49738a96abef - 2020-04-24 14:39:27
任务状态：celery@aa - task-succeeded - fc5d15ac-c1bc-4ca4-8f1b-3bf8d2415923 - 2020-04-24 14:39:27
任务状态：celery@aa - task-succeeded - ea2e1d39-1e2a-455f-9de8-49738a96abef - 2020-04-24 14:39:27
任务状态：celery@aa - task-received - d0ea2fd8-2b63-41bf-9c59-b7207e55bc7b - 2020-04-24 14:39:29
任务状态：celery@aa - task-retried - d0ea2fd8-2b63-41bf-9c59-b7207e55bc7b - 2020-04-24 14:39:29
任务状态：celery@aa - task-received - d0ea2fd8-2b63-41bf-9c59-b7207e55bc7b - 2020-04-24 14:39:30
任务状态：celery@aa - task-retried - d0ea2fd8-2b63-41bf-9c59-b7207e55bc7b - 2020-04-24 14:39:30
任务失败: None[d0ea2fd8-2b63-41bf-9c59-b7207e55bc7b] {'exception': 'TypeError("unsupported operand type(s) for +: \'int\' and \'str\'",)'}
任务状态：celery@aa - task-succeeded - c12dabe9-a927-463f-afc9-7a991fef73f7 - 2020-04-24 14:39:37

```

####  定时任务
- 添加 test_celery.py
> 我们通过设置 beat_schedule 参数，添加了两个任务调度，第一个名字 task_every_30_seconds，调用了 test_celery.add 任务，每隔 5 秒执行一次； 第二个名字 task_every_min，调用 test_celery.add 任务，每分钟执行一次。
```python
from celery.schedules import crontab
from datetime import timedelta
app.conf.timezone = 'Asia/Shanghai'
app.conf.beat_schedule = {
    'task_every_30_seconds': {    # 定时任务名称
        'task': 'test_celery.add',  # 调用 add 任务
        'schedule': timedelta(seconds=5),   # 每隔 5 秒执行一次
        'args': (23,  56)  # 作为参数传递进去
    },
    'task_every_min': {
        'task': 'test_celery.add',
        'schedule': crontab(minute='*'),    # 每分钟执行一次
        'args': (24, 57)
    }
}
```
- crontab 表达式语法

> 语法	含义
- crontab(minute=0, hour=0)	0:00 执行，
- crontab(minute=0, hour='*/3')	每隔 3 小时执行一次
- crontab(day_of_week='sunday')	星期日，每分钟执行一次
- crontab(day_of_month='2')	每月第二天执行，每分钟一次

> 关键词 beat， -l 指定日志级别为 debug
> 进程同样会一直占用终端，方便我们查看输出信息，正式环境使用 --detach  放置到后台
```text
(ops-py3venv) [ops@ops-3 ops2]$ celery -A test_celery beat -l debug
celery beat v4.3.0 (rhubarb) is starting.
__    -    ... __   -        _
LocalTime -> 2020-04-24 14:44:23
Configuration ->
    . broker -> redis://127.0.0.1:6379/3
    . loader -> celery.loaders.app.AppLoader
    . scheduler -> celery.beat.PersistentScheduler
    . db -> celerybeat-schedule
    . logfile -> [stderr]@%DEBUG
    . maxinterval -> 5.00 minutes (300s)
[2020-04-24 14:44:23,066: DEBUG/MainProcess] Setting default socket timeout to 30
[2020-04-24 14:44:23,067: INFO/MainProcess] beat: Starting...
[2020-04-24 14:44:23,156: DEBUG/MainProcess] Current schedule:
<ScheduleEntry: task_every_30_seconds test_celery.add(23, 56) <freq: 5.00 seconds>
<ScheduleEntry: task_every_min test_celery.add(24, 57) <crontab: * * * * * (m/h/d/dM/MY)>
[2020-04-24 14:44:23,156: DEBUG/MainProcess] beat: Ticking with max interval->5.00 minutes
[2020-04-24 14:44:23,157: DEBUG/MainProcess] beat: Waking up in 4.97 seconds.
[2020-04-24 14:44:28,131: DEBUG/MainProcess] beat: Synchronizing schedule...
[2020-04-24 14:44:28,170: INFO/MainProcess] Scheduler: Sending due task task_every_30_seconds (test_celery.add)
[2020-04-24 14:44:28,198: DEBUG/MainProcess] test_celery.add sent. id->e70d34b0-82e0-4031-9820-039182c0aa88
[2020-04-24 14:44:28,199: DEBUG/MainProcess] beat: Waking up in 4.93 seconds.
[2020-04-24 14:44:33,136: INFO/MainProcess] Scheduler: Sending due task task_every_30_seconds (test_celery.add)
[2020-04-24 14:44:33,138: DEBUG/MainProcess] test_celery.add sent. id->00c39bb3-70e6-42f6-8899-d8bad5c3976d
[2020-04-24 14:44:33,138: DEBUG/MainProcess] beat: Waking up in 4.99 seconds.
[2020-04-24 14:44:38,136: INFO/MainProcess] Scheduler: Sending due task task_every_30_seconds (test_celery.add)
[2020-04-24 14:44:38,144: DEBUG/MainProcess] test_celery.add sent. id->a42687c5-f1c7-4a0f-9526-22430d88d352
[2020-04-24 14:44:38,146: DEBUG/MainProcess] beat: Waking up in 4.98 seconds.

```

#### 任务队列
- 在两个终端开启两个 celery workers，指定不同队列 -Q queue_name1，queue_name2 
- 启动 celery worker 时指定队列, 参数 -Q 指定队列名称
- 一个 worker 启用多个队列，使用逗号分隔
```text
celery -A test_celery worker -Q lst1 -l info
...
celery -A test_celery worker -Q lst2 -l info
...
```
- 修改脚本
```text
# 任务队列
add.apply_async(
    (10, 100),  # 任务参数
    queue='lst1'  # 任务队列
)

add.apply_async(
    (20, 200),  # 任务参数
    queue='lst2'  # 任务队列
)
```
-  2个队列的返回结果
```text
                .> lst1             exchange=lst1(direct) key=lst1
               
[tasks]
  . task-add

[2020-04-24 14:47:10,974: INFO/MainProcess] Connected to redis://127.0.0.1:6379/3
[2020-04-24 14:47:10,982: INFO/MainProcess] mingle: searching for neighbors
[2020-04-24 14:47:12,001: INFO/MainProcess] mingle: all alone
[2020-04-24 14:47:12,036: INFO/MainProcess] celery@ops-3 ready.
[2020-04-24 14:50:37,611: INFO/MainProcess] Received task: task-add[e2581f00-22b1-4e93-ac1f-4e05d289bfe3]  
[2020-04-24 14:50:37,616: WARNING/ForkPoolWorker-1] 计算结果为： 110
[2020-04-24 14:50:37,640: WARNING/ForkPoolWorker-1] 任务执行成功
[2020-04-24 14:50:37,640: INFO/ForkPoolWorker-1] Task task-add[e2581f00-22b1-4e93-ac1f-4e05d289bfe3] succeeded in 0.02426284800094436s: 110
[2020-04-24 14:50:37,641: WARNING/ForkPoolWorker-1] 任务返回结果: <Context: {'lang': 'py', 'task': 'task-add', 'id': 'e2581f00-22b1-4e93-ac1f-4e05d289bfe3',
 'shadow': None, 'eta': None, 'expires': None, 'group': None, 'retries': 0, 'timelimit': [None, None], 'root_id': 'e2581f00-22b1-4e93-ac1f-4e05d289bfe3', 'parent_id': None, 'argsrepr': '(10, 100)', 'kwargsrepr': '{}', 'origin': 'gen13180@ops-3', 'reply_to': '7438a1f5-6c97-3908-9243-bc711027ce2f', 'correlation_id': 'e2581f00-22b1-4e93-ac1f-4e05d289bfe3', 'delivery_info': {'exchange': '', 'routing_key': 'lst1', 'priority': 0, 'redelivered': None}, 'args': [10, 100], 'kwargs': {}, 'hostname': 'celery@ops-3', 'is_eager': False, 'callbacks': None, 'errbacks': None, 'chain': None, 'chord': None, 'called_directly': False, '_protected': 1, '_children': []}>
```

```text
 -------------- [queues]
                .> lst2             exchange=lst2(direct) key=lst2
                

[tasks]
  . task-add

[2020-04-24 14:48:00,397: INFO/MainProcess] Connected to redis://127.0.0.1:6379/3
[2020-04-24 14:48:00,417: INFO/MainProcess] mingle: searching for neighbors
[2020-04-24 14:48:01,453: INFO/MainProcess] mingle: all alone
[2020-04-24 14:48:01,489: INFO/MainProcess] celery@ops-3 ready.
[2020-04-24 14:50:37,626: INFO/MainProcess] Received task: task-add[a0d9db68-e1ec-499b-b083-71491cd16496]  
[2020-04-24 14:50:37,639: WARNING/ForkPoolWorker-1] 计算结果为： 220
[2020-04-24 14:50:37,647: WARNING/ForkPoolWorker-1] 任务执行成功
[2020-04-24 14:50:37,648: INFO/ForkPoolWorker-1] Task task-add[a0d9db68-e1ec-499b-b083-71491cd16496] succeeded in 0.011156651000419515s: 220
[2020-04-24 14:50:37,649: WARNING/ForkPoolWorker-1] 任务返回结果: <Context: {'lang': 'py', 'task': 'task-add', 'id': 'a0d9db68-e1ec-499b-b083-71491cd16496',
 'shadow': None, 'eta': None, 'expires': None, 'group': None, 'retries': 0, 'timelimit': [None, None], 'root_id': 'a0d9db68-e1ec-499b-b083-71491cd16496', 'parent_id': None, 'argsrepr': '(20, 200)', 'kwargsrepr': '{}', 'origin': 'gen13180@ops-3', 'reply_to': '7438a1f5-6c97-3908-9243-bc711027ce2f', 'correlation_id': 'a0d9db68-e1ec-499b-b083-71491cd16496', 'delivery_info': {'exchange': '', 'routing_key': 'lst2', 'priority': 0, 'redelivered': None}, 'args': [20, 200], 'kwargs': {}, 'hostname': 'celery@ops-3', 'is_eager': False, 'callbacks': None, 'errbacks': None, 'chain': None, 'chord': None, 'called_directly': False, '_protected': 1, '_children': []}>
```

#### flower 监控
> 启动 3 个 worker，每个 worker 启动 4 个子进程
```shell script
ops-py3venv) [ops@ops-3 ops2]$  celery multi start 3 -A test_celery -l info -c 4 --pidfile=/tmp/celery_%n.pid -f /tmp/celery.log
celery multi v4.3.0 (rhubarb)
> Starting nodes...
	> celery1@ops-3: OK
	> celery2@ops-3: OK
	> celery3@ops-3: OK

```
- 启动 flower
```shell script
# -A 指定应用， --port 指定端口
$ celery flower -A test_celery --port=8080
```
- 脚本
```python
# 修改文件 test_sender.py
from test_celery import *

# 添加 100 个任务到 celery 中
for i in range(1, 100):
    add.apply_async((10, 30))
```
- web页面 
>效果
- ![image](https://github.com/MagePY27/P27N15/blob/master/img/flow1.png)
- ![image](https://github.com/MagePY27/P27N15/blob/master/img/flow2.png)

####  celery  命令
> report
- celery -A test_celery report 
> 查看活动队列
- celery -A test_celery inspect active_queues
> 状态
- celery -A test_celery inspect stats
> 报告
- celery -A test_celery inspect report 