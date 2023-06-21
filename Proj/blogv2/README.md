# blogv2

个人博客搭建2.0

## apps

- article 文章app
- show 用来展示页面的app
- comment 文章评论app
- message_board 站点留言板app
- user_statistics 用户统计app
- userinfo 个人信息app
- monitor 不是一个app，利用celery用来监控网站是否运行，如果未运行发送邮件到指定邮箱

## 项目启动

- 启动celery `celery -B -A monitor worker -l info`

## 主要技术

- Django rest framework + Vue + Bootstrap

## 总结

- 学习了drf后在原有的blog 1.0 版本上进行的更新，整体功能来说改变不大，只是重新重构了一下页面
- 基本没有使用django的模板（当然还是用到了一点点），前端使用vue获取数据并填充到页面中
- vue基本小白水平，还需很大提升
