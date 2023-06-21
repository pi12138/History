from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from design.rest.serializers import GraduationDesignSerializer, GraduationThesisSerializer, LocationSerializer, \
    GraduationReplySerializer
from design.models import GraduationDesign, GraduationThesis, GraduationReply
from organization.models import Location

import datetime


class GraduationDesignViewSet(ViewSet):
    """
    毕业设计视图： 通用功能
        - 学生： 上传毕业设计文件
        - 教师： 下载毕业设计文件 + 审阅毕业设计
        - 管理员： 查看毕业设计
    """

    def create(self, request):
        """
        学生功能： 上传毕业设计
        """
        query_dict = request.data
        data = dict()
        data['design'] = query_dict.get('file')
        data['upload_time'] = datetime.datetime.now()
        data['subject'] = request.user.student.select_student.id

        ser = GraduationDesignSerializer(data=data)
        if not ser.is_valid():
            return Response({'msg': "上传失败", 'error': ser.errors}, status=400)

        ser.save()
        return Response({'data': ser.data})

    def retrieve(self, request, pk=None):
        """
        通用功能： 查看毕业设计
        """
        ret = self.handle_pk(pk)
        if isinstance(ret, dict):
            return Response(ret, status=400)

        ser = GraduationDesignSerializer(instance=ret)

        return Response({'data': ser.data})

    def update(self, request, pk=None):
        """
        学生功能：修改毕业设计
        """
        ret = self.handle_pk(pk)
        if isinstance(ret, dict):
            return Response(ret, status=400)

        query_dict = request.data
        data = dict()
        data['design'] = query_dict.get('file')
        data['upload_time'] = datetime.datetime.now()
        data['subject'] = request.user.student.select_student.id
        ser = GraduationDesignSerializer(instance=ret, data=data)

        if not ser.is_valid():
            return Response({"msg": "修改毕业设计失败", 'error': ser.errors}, status=400)

        ser.save()
        return Response({'data': ser.data})

    def partial_update(self, request, pk=None):
        """
        教师功能：审阅毕业设计
        """
        ret = self.handle_pk(pk)
        if isinstance(ret, dict):
            return Response(ret, status=400)

        data = request.data
        data['review_time'] = datetime.datetime.now()

        ser = GraduationDesignSerializer(instance=ret, data=data)
        if not ser.is_valid():
            return Response({"msg": "审核毕业设计失败", 'error': ser.errors}, status=400)

        ser.save()
        return Response({'data': ser.data})

    def handle_pk(self, pk):
        if not pk:
            return {'msg': "未传入毕业设计参数"}

        query_set = GraduationDesign.objects.filter(pk=pk)
        if not query_set.exists():
            return {'msg': "毕业设计不存在"}

        return query_set[0]


class GraduationThesisViewSet(ViewSet):
    """
    通用功能: 毕业论文
        - 学生: 上传 + 下载 + 修改 + 查看毕业设计成绩
        - 教师: 审核 + 下载
        - 管理员: 查看
    """
    def create(self, request):
        """
        学生功能: 上传毕业论文
        """
        query_dict = request.data
        data = dict()
        data['thesis'] = query_dict.get('file')
        data['words'] = query_dict.get('words')
        data['summary'] = query_dict.get('summary')
        data['subject'] = request.user.student.select_student.id
        data['upload_time'] = datetime.datetime.now()

        ser = GraduationThesisSerializer(data=data)
        if not ser.is_valid():
            return Response({"msg": "创建毕业论文失败", 'error': ser.errors}, status=400)

        ser.save()
        return Response({'data': ser.data})

    def retrieve(self, request, pk=None):
        """
        通用功能: 查看毕业设计
        """
        ret = self.handle_pk(pk)
        if isinstance(ret, dict):
            return Response(ret, status=400)

        ser = GraduationThesisSerializer(instance=ret)

        return Response({"data": ser.data})

    def update(self, request, pk=None):
        """
        学生功能: 修改毕业论文
        """
        ret = self.handle_pk(pk)
        if isinstance(ret, dict):
            return Response(ret, status=400)

        query_dict = request.data
        data = dict()
        data['thesis'] = query_dict.get('file')
        data['words'] = query_dict.get('words')
        data['summary'] = query_dict.get('summary')
        data['subject'] = request.user.student.select_student.id
        data['upload_time'] = datetime.datetime.now()

        ser = GraduationThesisSerializer(instance=ret, data=data)
        if not ser.is_valid():
            return Response({'msg': "更新毕业论文失败", 'error': ser.errors}, status=400)

        ser.save()
        return Response({'data': ser.data})

    def partial_update(self, request, pk=None):
        """
        教师功能: 审核毕业设计
        """
        ret = self.handle_pk(pk)
        if isinstance(ret, dict):
            return Response(ret, status=400)

        data = request.data
        data['review_time'] = datetime.datetime.now()

        ser = GraduationThesisSerializer(instance=ret, data=data)
        if not ser.is_valid():
            return Response({'msg': "审核毕业论文失败", 'error': ser.errors}, status=400)

        ser.save()
        return Response({'data': ser.data})

    def handle_pk(self, pk):
        if not pk:
            return {'msg': "未传入毕业论文参数"}

        query_set = GraduationThesis.objects.filter(pk=pk)
        if not query_set.exists():
            return {'msg': "毕业论文不存在"}

        return query_set[0]

    @action(methods=['GET'], detail=False)
    def score(self, request):
        these = request.query_params.get('theseId')
        query_set = GraduationThesis.objects.filter(id=these)
        if not query_set.exists():
            return Response({'msg': '未找到论文成绩'}, status=400)

        these_obj = query_set[0]
        score = these_obj.score
        if score is None:
            score = '当前未给出论文成绩'

        return Response({'data': score})


class GraduationReplyViewSet(ViewSet):
    """
    毕业答辩地点
    """
    def list(self, request):
        query_set = Location.objects.all()
        ser = LocationSerializer(instance=query_set, many=True)
        return Response(ser.data)

    def create(self, request):
        data = request.data
        data['select_time'] = datetime.datetime.now()
        data['student'] = request.user.student.id

        ser = GraduationReplySerializer(data=data)
        if not ser.is_valid():
            return Response({'msg': '选择答辩地点失败', 'error': ser.errors}, status=400)

        ser.save()

        return Response({'data': ser.data})

    @action(methods=['GET'], detail=False)
    def location(self, request):
        student = request.user.student
        query_set = GraduationReply.objects.filter(student_id=student.id)
        if not query_set.exists():
            return Response({'msg': '未选择答辩地点', 'data': ''})

        location = query_set[0].location
        ser = LocationSerializer(instance=location)
        return Response({'data': ser.data})
