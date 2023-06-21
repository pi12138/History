# dailyfresh
Django实现的天天生鲜项目

- 在学习Django后,按照黑马的视频所写的一个项目
- 该项目内容包含了电商项目开发中使用到的大多数技术
- 实现功能：用户注册，用户登录，购物车，用户中心，首页，订单系统，地址信息管理，商品列表，商品详情，支付功能
- 使用技术：python + django + mysql + redis + celery + nginx + FastDFS分布式文件存储系统 + haystack全文检索

## 使用配置
- `django3.txt` 中是项目中需要使用的模块, `pip install -r django3.txt` 安装
- 项目使用 MySQL 数据库存储数据，使用 Redis 存储缓存，历史记录，购物车记录，所以需要下载MySQL，Redis, 并根据settings.py文件进行相应的配置
- 项目使用 celery 生成静态页面和发送邮件，要想使用该功能，需要先安装 celery 并启动
- 项目使用的第三方的文件存储系统 FastDFS 也需要下载进行相应的配置
