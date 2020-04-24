# 修改文件 test_sender.py
from test_celery import *

# 添加 100 个任务到 celery 中
for i in range(1, 100):
    add.apply_async((10, 30))
