from django.db import models
from apps.user_statistics.models import UserInterviewInfo
# Create your models here.


class Article(models.Model):
    """博客文章模型类"""
    title = models.CharField(max_length=100, verbose_name="博客标题", unique=True)
    # category = models.CharField(max_length=50, verbose_name="博客标签")
    category = models.ForeignKey('ArticleCategory', on_delete=models.CASCADE, verbose_name="博客标签")
    pub_date = models.DateTimeField(auto_now_add=True, editable=True, verbose_name="发布时间")
    update_time = models.DateTimeField(auto_now=True, null=True, verbose_name="更新时间")
    content = models.TextField(blank=True, null=True, verbose_name="博客正文")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "博客"
        verbose_name_plural = verbose_name

    def article_url(self):
        return "http://127.0.0.1:8000/api/blogv2/articles/{}/".format(self.pk)
    
    def category_name(self):
        return self.category.name

    def update_time_handler(self):
        return self.update_time.strftime("%Y-%m-%d")

    def article_read_number(self):
        url = "/api/blogv2/articles/{}/".format(self.pk)
        number = UserInterviewInfo.objects.filter(interview_url=url).count()
        return number
    
    def article_comment_number(self):
        number = self.comment_set.all().count()
        return number


class ArticleCategory(models.Model):
    """博文文章标签"""
    name = models.CharField(max_length=100, verbose_name="博客分类", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "文章标签"
        verbose_name_plural = verbose_name


