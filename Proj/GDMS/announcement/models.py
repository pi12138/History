from django.db import models

# Create your models here.
from user.models import Administrator


class Announcement(models.Model):
    """
    公告模型
    """
    title = models.CharField(verbose_name="标题", max_length=100, blank=True, null=True)
    publisher = models.ForeignKey(verbose_name="发布人", to=Administrator, on_delete=models.CASCADE)
    publish_time = models.DateTimeField(verbose_name="发布时间", blank=True, null=True)
    publish_content = models.TextField(verbose_name="发布内容", blank=True, null=True)
    publish_file = models.FileField(verbose_name="发布文件", upload_to="announcement")
