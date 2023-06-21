from django.contrib import admin
from apps.myblog.models import Article

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'pub_date', 'update_time']


admin.site.register(Article, ArticleAdmin)
