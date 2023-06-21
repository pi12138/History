from django.db import models

# Create your models here.
from user.models import Teacher, Student, Administrator


class Subject(models.Model):
    """
    课题模型
    """
    REVIEW_RESULT_VALUE = (
        (0, "待审核"),
        (1, "审核通过"),
        (2, "审核未通过")
    )

    subject_name = models.CharField(verbose_name="课题名称", max_length=100)
    questioner = models.ForeignKey(to=Teacher, on_delete=models.CASCADE, verbose_name="出题人")
    number_of_people = models.IntegerField(verbose_name="课题人数", default=1)
    select_student = models.OneToOneField(to=Student, on_delete=models.CASCADE, verbose_name="选题学生", blank=True,
                                          null=True, related_name='select_student')
    subject_description = models.TextField(verbose_name="课题描述")
    expected_goal = models.TextField(verbose_name="预期目标")
    require = models.TextField(verbose_name="对学生知识和能力的要求")
    required_conditions = models.TextField(verbose_name="所需条件")
    references = models.TextField(verbose_name="参考资料")
    declare_time = models.DateTimeField(verbose_name="申报时间", auto_now=True,)
    reviewer = models.ForeignKey(Administrator, on_delete=models.CASCADE, verbose_name="审核人", blank=True, null=True)
    review_result = models.IntegerField(choices=REVIEW_RESULT_VALUE, default=0, verbose_name="审核结果", blank=True,
                                        null=True)
    review_time = models.DateTimeField(verbose_name="审核时间", blank=True, null=True)
    review_reason = models.TextField(verbose_name="审批理由", blank=True, null=True)
    # apply_students = models.OneToOneField(verbose_name="申请学生", to=Student, on_delete=models.CASCADE, blank=True,
    #                                       null=True, related_name='apply_students')

    def __str__(self):
        return self.subject_name


class ApplySubject(models.Model):
    """
    学生申请记录模型
    """
    APPLY_RESULT_VALUE = (
        (0, '待审核'),
        (1, "申请通过"),
        (2, "申请未通过")
    )

    subject = models.ForeignKey(verbose_name="申请的课题", to=Subject, on_delete=models.CASCADE, blank=True, null=True)
    student = models.ForeignKey(verbose_name="申请学生", to=Student, on_delete=models.CASCADE, blank=True, null=True)
    apply_time = models.DateTimeField(verbose_name="申请时间", blank=True, null=True)
    apply_result = models.IntegerField(verbose_name="申请结果", default=0)

    def __str__(self):
        return "{}---{}".format(self.subject, self.student)


class TaskBook(models.Model):
    """
    任务书模型
    """
    REVIEW_RESULT_VALUE = (
        (0, '待审核'),
        (1, '合格'),
        (2, '不合格')
    )

    subject = models.OneToOneField(Subject, verbose_name="所属课题", on_delete=models.CASCADE, related_name='task_book')
    release_time = models.DateTimeField(verbose_name="任务书下达时间")
    subject_desc = models.TextField(verbose_name="课题简述", default="", blank=True, null=True)
    purpose_and_significance = models.TextField(verbose_name="研究的目的意义", default="", blank=True, null=True)
    content_and_technology = models.TextField(verbose_name="主要的内容和技术", default="", blank=True, null=True)
    data_and_information = models.TextField(verbose_name="原始的数据和资料", default="", blank=True, null=True)
    schedule = models.TextField(verbose_name="进度安排", default="", blank=True, null=True)
    references = models.TextField(verbose_name="参考资料", default="", blank=True, null=True)
    information_in_English = models.TextField(verbose_name="英文资料翻译要求", default="", blank=True, null=True)
    reviewer = models.ForeignKey(Administrator, verbose_name="审核人", on_delete=models.CASCADE, blank=True, null=True)
    review_time = models.DateTimeField(verbose_name="审核时间", blank=True, null=True)
    review_result = models.IntegerField(verbose_name="审核结果", choices=REVIEW_RESULT_VALUE, default=0)

    def __str__(self):
        return "{}的任务书".format(self.subject)


