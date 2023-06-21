from django.db import models

# Create your models here.
from subject.models import Subject
from organization.models import Location
from user.models import Student


class GraduationDesign(models.Model):
    """
    毕业设计模型
    """
    subject = models.OneToOneField(verbose_name="课题", to=Subject, on_delete=models.CASCADE)
    design = models.FileField(verbose_name='毕业设计文件', upload_to="design/", blank=True, null=True)
    upload_time = models.DateTimeField(verbose_name="上传时间", blank=True, null=True)
    review_option = models.TextField(verbose_name="指导老师审核意见", blank=True, null=True)
    review_time = models.DateTimeField(verbose_name="审阅时间", blank=True, null=True)

    def __str__(self):
        return "{}的毕业设计文件".format(self.subject)


class GraduationThesis(models.Model):
    """
    毕业论文模型
    """

    subject = models.OneToOneField(verbose_name="课题", to=Subject, on_delete=models.CASCADE)
    words = models.CharField(verbose_name="关键词", max_length=250)
    summary = models.TextField(verbose_name="摘要", blank=True, null=True)
    thesis = models.FileField(verbose_name="毕业论文文件", upload_to="thesis/", blank=True, null=True)
    upload_time = models.DateTimeField(verbose_name="上传时间", blank=True, null=True)
    review_option = models.TextField(verbose_name="指导老师审核意见", blank=True, null=True)
    review_time = models.DateTimeField(verbose_name="审阅时间", blank=True, null=True)
    score = models.IntegerField(verbose_name="论文成绩", blank=True, null=True)

    def __str__(self):
        return "{}的毕业论文".format(self.subject)


class GraduationReply(models.Model):
    """
    毕业答辩模型
    """
    location = models.OneToOneField(verbose_name="答辩地点", to=Location, on_delete=models.CASCADE)
    student = models.OneToOneField(verbose_name='答辩学生', to=Student, on_delete=models.CASCADE)
    select_time = models.DateTimeField(verbose_name='选择时间')

    def __str__(self):
        return self.location.location_number
