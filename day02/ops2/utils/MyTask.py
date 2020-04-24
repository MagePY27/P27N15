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
