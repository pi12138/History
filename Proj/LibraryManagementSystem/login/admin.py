from django.contrib import admin
from .models import *
# Register your models here.


# admin.site.register(UserInfo)


class UserInfoAdmin(admin.ModelAdmin):
    # list_display = ['user_account', 'user_password', 'user_age', 'user_sex', 'user_phone']
    list_display = ['account', 'password', 'age', 'sex', 'phone']
    search_fields = ['user_account']
    list_per_page = 10
    list_filter = ['user_age', 'user_sex']


class BookInfoAdmin(admin.ModelAdmin):
    list_display = ['isbn', 'name', 'author', 'publish', 'date', 'num']
    list_per_page = 10
    list_filter = ['book_author', 'book_publish']
    search_fields = ['book_name', 'book_author']


class BorrowInfoAdmin(admin.ModelAdmin):
    list_display = ['borrower', 'book', 'borrowing', 'return_']
    list_per_page = 10
    list_filter = ['borrower_id', 'book_id']
    # 因为borrower_id,与book_id均为外键，所以查询时需要查询关联表中的字段
    # borrower_id__user_account 中间的下划线为两个！！！
    search_fields = ['borrower_id__user_account', 'book_id__ISBN']


admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(BorrowInfo, BorrowInfoAdmin)

# 修改站点默认字段
admin.site.site_title = "图书管理系统后台管理"
admin.site.site_header = "图书管理系统后台管理"
admin.site.index_title = "数据表"
