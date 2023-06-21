from django.db import models

# Create your models here.
from subject.models import Subject
from user.models import Teacher


class Report(models.Model):
    """
    开题报告模型
    Research Status
Feasibility Analysis
Problems and solutions
Project working conditions
Programme and schedule
    """
    REVIEW_RESULT_VALUE = (
        (0, "待审阅"),
        (1, "合格"),
        (2, "不合格")
    )

    subject = models.OneToOneField(verbose_name='课题', to=Subject, on_delete=models.CASCADE)
    submit_time = models.DateTimeField(verbose_name='提交时间', blank=True, null=True)
    research_status = models.TextField(verbose_name='研究现状综述', blank=True, null=True)
    feasibility_analysis = models.TextField(verbose_name='可行性分析', blank=True, null=True)
    problems_and_solutions = models.TextField(verbose_name='重点/关键问题及解决思路', blank=True, null=True)
    working_conditions = models.TextField(verbose_name='课题工作条件', blank=True, null=True)
    programme_and_schedule = models.TextField(verbose_name='工作方案及进度安排', blank=True, null=True)
    guide_teacher = models.OneToOneField(verbose_name="指导老师", to=Teacher, on_delete=models.CASCADE, blank=True, null=True)
    review_opinion = models.TextField(verbose_name="审阅意见", blank=True, null=True)
    review_time = models.DateTimeField(verbose_name="审阅时间", blank=True, null=True)
    review_result = models.IntegerField(verbose_name="审核结果", choices=REVIEW_RESULT_VALUE, default=0)

