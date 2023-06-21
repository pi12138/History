from django.db import models

# Create your models here.


class UserInfo(models.Model):
    YES_OR_NO = (
        (1, 'YES'),
        (0, "NO"),
    )

    name = models.CharField(max_length=30, verbose_name="姓名")
    nickname = models.CharField(max_length=30, verbose_name="昵称")
    github = models.URLField(verbose_name="github地址", max_length=200)
    email = models.EmailField(max_length=200, verbose_name="邮箱")
    location = models.CharField(max_length=30, verbose_name="地理位置")
    avatar = models.FileField(upload_to='media/userinfo_image/', max_length=200, verbose_name="头像")
    words = models.TextField(verbose_name="想说啥")
    used = models.IntegerField(choices=YES_OR_NO, default=0, verbose_name="使用")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "个人信息"
        verbose_name_plural = verbose_name
