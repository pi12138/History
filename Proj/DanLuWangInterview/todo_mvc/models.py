from django.db import models

# Create your models here.


class Task(models.Model):
    """
    任务模型
    """
    TASK_STATUS_VALUE = (
        (0, 'active'),
        (1, 'completed')
    )

    title = models.CharField(max_length=100, verbose_name="任务标题", unique=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建任务时间")
    status = models.IntegerField(choices=TASK_STATUS_VALUE, default=0, verbose_name="任务状态")
    # completed_time = models.DateTimeField(default=None, blank=True, null=True, verbose_name="任务完成时间")
    is_deleted = models.BooleanField(default=False, verbose_name="是否已删除")
