from django.db import models

# Create your models here.
from tinymce.models import HTMLField


class Article(models.Model):
    """博客文章模型类"""
    title = models.CharField(max_length=100, verbose_name="博客标题")
    category = models.CharField(max_length=50, verbose_name="博客标签")
    pub_date = models.DateTimeField(auto_now_add=True, editable=True, verbose_name="发布时间")
    update_time = models.DateTimeField(auto_now=True, null=True, verbose_name="更新时间")
    content = models.TextField(blank=True, null=True, verbose_name="博客正文")
    # comment_number = models.IntegerField(default=0, verbose_name="评论数")
    # content = HTMLField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "博客"
        verbose_name_plural = verbose_name

