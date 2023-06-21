from django.db import models
from django.contrib.auth.models import User
from organization.models import Faculty, Profession, Direction, Klass, Office
# Create your models here.


# class Account(models.Model):
#     """
#     账号模型
#     """
#     username = models.CharField(verbose_name="账号名", max_length=30, unique=True)
#     password = models.CharField(max_length=30, verbose_name="密码")
#     email = models.CharField(max_length=30, verbose_name="邮箱")
#     is_active = models.BooleanField(default=False, verbose_name="是否激活")


class Student(models.Model):
    """
    学生模型
    """
    GENDER = (
        (0, '男'), 
        (1, '女'))

    name = models.CharField(max_length=30, verbose_name="学生姓名")
    gender = models.IntegerField(choices=GENDER, verbose_name="性别", default=0)
    klass = models.ForeignKey(to=Klass, on_delete=models.CASCADE, verbose_name="班级", blank=True, null=True)
    diretcion = models.ForeignKey(to=Direction, on_delete=models.CASCADE, verbose_name="方向", blank=True, null=True)
    profession = models.ForeignKey(to=Profession, on_delete=models.CASCADE, verbose_name="专业", blank=True, null=True)
    faculty = models.ForeignKey(to=Faculty, on_delete=models.CASCADE, verbose_name="学院", blank=True, null=True)
    phone = models.CharField(max_length=30, verbose_name="联系方式")
    qq = models.CharField(max_length=30, verbose_name="QQ")
    # account = models.ForeignKey(to=Account, on_delete=models.CASCADE, verbose_name="账户")
    is_monitor = models.BooleanField(default=False, verbose_name="是否是班长")
    account = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name='账户')

    def __str__(self):
        return self.name


class Teacher(models.Model):
    """
    老师模型
    """
    GENDER = (
        (0, '男'), 
        (1, '女'))

    EDUCTATION_VALUES = (
        (0, "学士"),
        (1, "硕士"),
        (2, '博士')
    )
    
    TEACHER_TITLE = (
        (0, "助教"),
        (1, "讲师"),
        (2, "副教授"),
        (3, "教授")
    )
    
    name = models.CharField(max_length=30, verbose_name="姓名")
    gender = models.IntegerField(choices=GENDER, verbose_name="性别", default=0)
    education = models.IntegerField(choices=EDUCTATION_VALUES, verbose_name="学历", default=1)
    teacher_title = models.IntegerField(choices=TEACHER_TITLE, verbose_name="职称", default=1)
    phone = models.CharField(max_length=30, verbose_name="联系方式")
    qq = models.CharField(max_length=30, verbose_name="QQ")
    office = models.ForeignKey(to=Office, on_delete=models.CASCADE, verbose_name="教研室", blank=True, null=True)
    faculty = models.ForeignKey(to=Faculty, on_delete=models.CASCADE, verbose_name="学院", blank=True, null=True)
    # account = models.ForeignKey(to=Account, on_delete=models.CASCADE, verbose_name="账户")
    is_monitor = models.BooleanField(default=False, verbose_name="是否是教研室负责人")
    account = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name='账户')

    def __str__(self):
        return self.name


class Administrator(models.Model):
    """
    管理员模型
    """
    faculty = models.ForeignKey(to=Faculty, on_delete=models.CASCADE, verbose_name="学院", blank=True, null=True)
    # account = models.ForeignKey(to=Account, on_delete=models.CASCADE, verbose_name="账户")
    account = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name='账户')
    name = models.CharField(verbose_name="姓名", max_length=30, default="", blank=True, null=True)

    def __str__(self):
        return self.name
