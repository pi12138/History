from django.contrib import admin
from help.models import *
# Register your models here.


class FeedBackInfoAdmin(admin.ModelAdmin):
    """意见反馈类"""
    list_display = ['account', 'opinion', 'issuing']
    list_per_page = 10
    list_filter = ['user_account']
    search_fields = ['user_account']


admin.site.register(FeedBackInfo, FeedBackInfoAdmin)
