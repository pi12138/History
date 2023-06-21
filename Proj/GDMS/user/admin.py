from django.contrib import admin
from user import models
# Register your models here.


admin.site.register(models.Administrator)
admin.site.register(models.Student)
admin.site.register(models.Teacher)


admin.site.site_header = "毕业设计管理系统"
admin.site.site_title = "毕业设计管理系统"
# admin.site.index_title = "毕业设计管理系统"