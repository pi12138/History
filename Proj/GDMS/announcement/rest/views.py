from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from announcement.models import Announcement
from announcement.rest.serializers import AnnouncementSerializer
from announcement.rest.paginations import CustomPageiantion

import datetime


class AnnouncementViewSet(ViewSet):
    """
    通用功能:
        - 管理员: 发布公告
        - 学生: 查看公告
        - 教师: 查看公告
    """

    def create(self, request):
        """
        管理员: 创建公告
        """
        form_data = request.data
        data = dict()
        data['title'] = form_data.get('title')
        data['publisher'] = request.user.administrator.id
        data['publish_time'] = datetime.datetime.now()
        data['publish_content'] = form_data.get('publish_content')
        data['publish_file'] = form_data.get('file', None)

        ser = AnnouncementSerializer(data=data)
        if not ser.is_valid():
            return Response({'msg': "创建公告失败", 'error': ser.errors}, status=400)

        ser.save()
        return Response({'data': ser.data})

    def update(self, request, pk=None):
        """
        管理员: 修改公告
        """
        if not pk:
            return Response({'msg': '未传入公告参数'}, status=400)

        query_set = Announcement.objects.filter(pk=pk)
        if not query_set.exists():
            return Response({'msg': "该公告不存在"}, status=400)

        form_data = request.data
        data = dict()
        data['title'] = form_data.get('title')
        data['publisher'] = request.user.administrator.id
        data['publish_time'] = datetime.datetime.now()
        data['publish_content'] = form_data.get('publish_content')
        data['publish_file'] = form_data.get('file')

        ser = AnnouncementSerializer(instance=query_set[0], data=data)
        if not ser.is_valid():
            return Response({'msg': "修改公告失败", 'error': ser.errors}, status=400)

        ser.save()
        return Response({'data': ser.data})

    def retrieve(self, request, pk=None):
        """
        查看公告
        """
        if not pk:
            return Response({'msg': '未传入公告参数'}, status=400)

        query_set = Announcement.objects.filter(pk=pk)
        if not query_set.exists():
            return Response({'msg': "该公告不存在"}, status=400)

        ser = AnnouncementSerializer(instance=query_set[0])

        return Response({'data': ser.data})

    def list(self, request):
        """
        公告列表
        """
        query_set = Announcement.objects.all()

        page_obj = CustomPageiantion()
        page_res = page_obj.paginate_queryset(queryset=query_set, request=request, view=self)
        ser = AnnouncementSerializer(instance=page_res, many=True)

        return page_obj.get_paginated_response(ser.data)

    def destroy(self, requets, pk=None):
        """
        管理员: 删除公告
        """
        if not pk:
            return Response({'msg': '未传入公告参数'}, status=400)

        query_set = Announcement.objects.filter(pk=pk)
        if not query_set.exists():
            return Response({'msg': "该公告不存在"}, status=400)

        query_set.delete()

        return Response({'msg': "删除成功"})
