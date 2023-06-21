from django.db import models

# Create your models here.


class MessageBoardModel(models.Model):
    """
    留言板模型类
    """
    email = models.CharField(max_length=30, verbose_name="邮箱")
    content = models.TextField(blank=True, null=True, verbose_name="留言内容")
    pub_date = models.DateTimeField(auto_now_add=True, editable=True, verbose_name="发布时间")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "留言板"
        verbose_name_plural = verbose_name