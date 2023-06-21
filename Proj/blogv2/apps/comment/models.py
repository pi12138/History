from django.db import models
from apps.article.models import Article
# Create your models here.


class Comment(models.Model):
    """文章评论模型类"""
    email = models.CharField(max_length=30, null=True, blank=True, verbose_name='邮箱')
    content = models.TextField(blank=True, null=True, verbose_name='评论内容')
    pub_date = models.DateTimeField(auto_now_add=True, editable=True, verbose_name='评论时间')
    article = models.ForeignKey(Article, verbose_name='文章title', on_delete=models.CASCADE)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name
