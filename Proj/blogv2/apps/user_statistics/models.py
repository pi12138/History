from django.db import models
import requests
# Create your models here.


class UserIP(models.Model):
    """
    访问用户IP模型类
    """
    ip = models.CharField(verbose_name="IP地址", max_length=50, unique=True)
    ip_addr = models.CharField(verbose_name="IP地理位置", max_length=100, default="")
    count = models.IntegerField(verbose_name="访问次数", default=0)

    class Meta:
        verbose_name = "用户访问信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip

    def get_addr(self):
        url = "http://freeapi.ipip.net/{}".format(self.ip)
        addr_list = requests.get(url).json()
        addr_str = "-".join(addr_list)
        return addr_str


class UserInterviewInfo(models.Model):
    """
    用户访问信息模型类
    """
    ip = models.ForeignKey('UserIP', on_delete=models.CASCADE, verbose_name="用户IP地址")
    interview_time = models.DateTimeField(auto_now_add=True, editable=True, verbose_name="访问时间")
    interview_url = models.CharField(max_length=100, verbose_name="访问地址", default="")

    def __str__(self):
        return self.ip

        