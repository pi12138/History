from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from django.db.models import Q

from message_board.models import MessageBoard
from message_board.rest.serializers import MessageBoardSerializer
from announcement.rest.paginations import CustomPageiantion

import datetime


class MessageBoardViewSet(ViewSet):
    """
    留言板功能:
        - 学生: 发表 + 查案
        - 教师: 查看 + 发表
        - 管理员: 查看
    """
    def list(self, request):
        """
        留言列表
        """
        user = request.query_params.get('user_id', 0)

        if not user:
            return Response({'msg': '请传入用户参数'}, status=400)

        q1 = Q(publisher_id=user)
        q2 = Q(receiver_id=user)

        query_set = MessageBoard.objects.filter(q1 | q2)
        page_obj = CustomPageiantion()
        page_data = page_obj.paginate_queryset(queryset=query_set, request=request, view=self)
        ser = MessageBoardSerializer(instance=page_data, many=True)

        return page_obj.get_paginated_response(ser.data)

    def retrieve(self, request, pk=None):
        """
        单个留言详情
        """
        if not pk:
            return Response({'msg': "未传入消息参数"}, status=400)

        query_set = MessageBoard.objects.filter(pk=pk)
        if not query_set.exists():
            return Response({'msg': "该留言不存在"}, status=400)

        ser = MessageBoardSerializer(instance=query_set[0])

        return Response({'data': ser.data})

    def create(self, request):
        """
        创建留言
        """
        query_dict = request.data

        data = dict()
        data['title'] = query_dict.get('title')
        data['content'] = query_dict.get('content')
        data['annex'] = query_dict.get('file', None)
        data['publish_time'] = datetime.datetime.now()
        data['publisher'] = query_dict.get('publisher')
        data['receiver'] = query_dict.get('receiver')

        ser = MessageBoardSerializer(data=data)
        if not ser.is_valid():
            return Response({"msg": "创建留言失败", 'error': ser.errors}, status=400)

        ser.save()
        return Response({'data': ser.data})

    @action(methods=["GET"], detail=True)
    def read_message(self, request, pk=None):
        """设置消息已读"""
        if not pk:
            return Response({'msg': "未传入消息参数"}, status=400)

        query_set = MessageBoard.objects.filter(pk=pk)
        if not query_set.exists():
            return Response({'msg': "该留言不存在"}, status=400)

        obj = query_set[0]
        obj.is_read = True
        obj.save()
        return Response({'msg': "设置成功"})

    @action(methods=['POST'], detail=True)
    def reply_message(self, request, pk=None):
        """
        教师功能: 回复留言
        """
        if not pk:
            return Response({'msg': "未传入消息参数"}, status=400)

        query_set = MessageBoard.objects.filter(pk=pk)
        if not query_set.exists():
            return Response({'msg': "该留言不存在"}, status=400)

        query_dict = request.data
        teacher = request.user.teacher

        data = dict()
        data['title'] = query_dict.get('title')
        data['content'] = query_dict.get('content')
        data['annex'] = query_dict.get('file', None)
        data['publish_time'] = datetime.datetime.now()
        data['publisher'] = teacher.id
        data['receiver'] = query_dict.get('receiver')

        ser = MessageBoardSerializer(data=data)
        if not ser.is_valid():
            return Response({"msg": "创建回复失败", 'error': ser.errors}, status=400)

        ser.save()
        return Response({'data': ser.data})

    @action(methods=["GET"], detail=False)
    def publish_message(self, request):
        """发出的消息"""
        user = request.user

        query_set = MessageBoard.objects.filter(publisher_id=user.id).order_by('is_read', '-publish_time')
        page_obj = CustomPageiantion()
        data = page_obj.paginate_queryset(queryset=query_set, request=request, view=self)
        ser = MessageBoardSerializer(instance=data, many=True)

        return page_obj.get_paginated_response(ser.data)

    @action(methods=['GET'], detail=False)
    def receive_message(self, request):
        """收到的消息"""
        user = request.user

        query_set = MessageBoard.objects.filter(receiver_id=user.id).order_by('is_read', '-publish_time')
        page_obj = CustomPageiantion()
        data = page_obj.paginate_queryset(queryset=query_set, request=request, view=self)
        ser = MessageBoardSerializer(instance=data, many=True)

        return page_obj.get_paginated_response(ser.data)

