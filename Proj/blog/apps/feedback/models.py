from django.db import models

# Create your models here.


class FeedBack(models.Model):
    """Blog留言模型类"""
    email = models.CharField(max_length=30, verbose_name='留言用户邮箱')
    content = models.TextField(blank=True, null=True, verbose_name='留言内容')
    pub_date = models.DateTimeField(auto_now_add=True, editable=True, verbose_name='留言时间')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Blog留言'
        verbose_name_plural = verbose_name
