from django.db import models

# Create your models here.


class FeedBackInfo(models.Model):
    user_account = models.CharField(max_length=12)
    opinion_content = models.TextField()
    issuing_time = models.DateTimeField()

    def __str__(self):
        return self.user_account

    class Meta:
        db_table = "feedback_info"

    def account(self):
        return self.user_account

    def opinion(self):
        return self.opinion_content

    def issuing(self):
        return self.issuing_time

    account.short_description = "账户"
    opinion.short_description = "意见"
    issuing.short_description = "发表时间"
