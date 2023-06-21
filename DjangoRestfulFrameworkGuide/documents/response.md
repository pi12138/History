# response

- "rest_framework.response.Response"
- 该类允许你根据客户端请求返回不同的表现形式（如： JSON ，HTML 等）
- 一般情况情况下传入一个data参数，然后返回Response的实例化对象就好了
- 允许传入一个status_code设置状态码。

## 需要注意

- 传入给Response的data参数通常是一个较为简单的数据类型，Response 类使用的渲染器不能处理复杂的数据类型（例如:django 模型)
- 通常data是一个python的常用数据类型

- response 暂时没有什么好写的，后面发现了新东西在补充。