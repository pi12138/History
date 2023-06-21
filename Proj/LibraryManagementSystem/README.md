# LibraryManagementSystem
基于Django的简单图书管理系统

- django.txt 中有项目所需要的Python包，下载后创建新的Python虚拟环境`pip install -r django.txt`安装
- 更改 settings.py 中的MySQL数据库配置
- 在自己的MySQL数据库中`create database library_management_system`新建一个数据库
- 进入虚拟环境，cd到项目目录下，生成数据库迁移文件`python manage.py makemigrations`, 执行迁移文件在数据库中生成表`python manage.py migrate`
- 运行项目`python manage.py runserver`
