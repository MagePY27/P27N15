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


# 定义一个任务，名字为 add
@app.task(bind=True, base=MyTask, name='task-add', max_retries=3)
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

# @app.task(bind=True, max_retries=3)  # 最大重试 3 次
# def test_retry(self):
#     print('执行 Celery 重试')
#     raise self.retry(countdown=1)  # 1 秒后执行重试
#
#
# @app.task(bind=True)
# def test_fail(self):
#     print('执行 Celery 失败')
#     raise RuntimeError('测试 celery 失败')

