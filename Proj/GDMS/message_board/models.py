from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class MessageBoard(models.Model):
    """
    留言板模型
    """
    title = models.CharField(verbose_name="标题", max_length=100, blank=True, null=True)
    content = models.TextField(verbose_name="主要内容", blank=True, null=True)
    annex = models.FileField(verbose_name="附件", upload_to='message/', blank=True, null=True)
    publish_time = models.DateTimeField(verbose_name="发表时间", blank=True, null=True)
    publisher = models.ForeignKey(verbose_name="发表人", to=User, on_delete=models.CASCADE,
                                  related_name='message_board_publisher')
    receiver = models.ForeignKey(verbose_name="接收人", to=User, on_delete=models.CASCADE,
                                 related_name='messsage_board_receiver')
    is_read = models.BooleanField(verbose_name="是否已读", default=False)

    def __str__(self):
        return self.title
