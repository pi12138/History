from django.contrib import admin
from apps.feedback.models import FeedBack
# Register your models here.


class FeedBackAdmin(admin.ModelAdmin):
    list_display = ['email', 'content', 'pub_date']


admin.site.register(FeedBack, FeedBackAdmin)