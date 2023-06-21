from django.contrib import admin
from apps.comment.models import Comment
# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    list_display = ['email', 'pub_date', 'article', 'content']


admin.site.register(Comment, CommentAdmin)