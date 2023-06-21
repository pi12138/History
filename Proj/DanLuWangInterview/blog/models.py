from django.db import models

# Create your models here.


class Article(models.Model):
    """
    文章模型类
    """
    title = models.CharField(max_length=100, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    create_time = models.DateTimeField(verbose_name="创建时间")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "博客"
        verbose_name_plural = verbose_name


class Comment(models.Model):
    """
    评论模型类
    """
    user_ip = models.CharField(max_length=100, verbose_name="评论人Ip")
    user_address = models.CharField(max_length=100, verbose_name="评论人地址")
    content = models.TextField(verbose_name="评论内容")
    email = models.CharField(max_length=100, verbose_name="邮箱", blank=True, null=True)
    create_time = models.DateTimeField(verbose_name="评论时间")
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, verbose_name="文章")

    def __str__(self):
        return self.user_ip

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name
