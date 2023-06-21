from rest_framework.viewsets import ViewSet
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
import datetime

from django.core.paginator import Paginator
from django.db.models import Q

from subject.models import Subject, ApplySubject, TaskBook
from .serializers import SubjectSerializer, ApplySubjectSerializer, SubjectInfoSerializer, TaskBookSerializer


class PendingSubjectViewSet(ViewSet):
    """
    管理员功能： 待审批课题
    """

    def list(self, request):

        query_set = Subject.objects.filter(review_result=0).order_by('-declare_time')
        ser = SubjectSerializer(instance=query_set, many=True)
        res = self.pagination(ser.data, request)

        return Response(res)

    def partial_update(self, request, pk=None):

        data = request.data
        subjects = Subject.objects.filter(id=pk)
        if not subjects.exists():
            return Response({'error': '当前课题不存在！'}, status=400)

        data['reviewer'] = request.user.administrator.id
        data['review_time'] = datetime.datetime.now()

        ser = SubjectSerializer(instance=subjects[0], data=data)
        if not ser.is_valid():
            return Response({'error': "发生错误", 'error_code': ser.errors}, status=400)

        ser.save()
        return Response({'data': ser.data, 'msg': '审核成功'})

    @staticmethod
    def pagination(data, request):
        page = request.query_params.get('page', 1)
        page = int(page)
        path = request.path

        if page < 1:
            page = 1

        paginator = Paginator(data, 10)
        num_pages = paginator.num_pages

        if page > num_pages:
            page = num_pages

        pa = paginator.page(page)
        obj_list = pa.object_list
        count = pa.paginator.count

        previous_url = '{}?page={}'.format(path, page - 1)
        next_url = '{}?page={}'.format(path, page + 1)
        if page == 1:
            previous_url = None

        if page == num_pages:
            next_url = None

        response_data = {
            'results': obj_list,
            'next_url': next_url,
            'previous_url': previous_url,
            'count': count,
            'num_pages': num_pages,
            'page': pa.number
        }

        return response_data


class PassedSubjectViewSet(ViewSet):
    """
    管理员功能：审核通过课题
    """

    def list(self, request):
        query_set = Subject.objects.filter(review_result=1)
        ser = SubjectSerializer(instance=query_set, many=True)
        res = PendingSubjectViewSet.pagination(ser.data, request)

        return Response(res)


class SelectSubjectViewSet(ViewSet):
    """
    学生模块： 选择课题
    """

    def list(self, request):
        subject_name = request.query_params.get('subject_name', "")
        office = int(request.query_params.get('office', 0))
        questioner = request.query_params.get('questioner', "")

        q1 = Q()
        q2 = Q()
        q3 = Q()
        if subject_name:
            q1 = Q(subject_name__icontains=subject_name)

        if office:
            q2 = Q(questioner__office_id=office)

        if questioner:
            q3 = Q(questioner__name__icontains=questioner)

        print(q1, q2, q3)
        query_set = Subject.objects.filter(q1, q2, q3, review_result=1)
        ser = SubjectSerializer(instance=query_set, many=True)
        res = PendingSubjectViewSet.pagination(ser.data, request)

        return Response(res)

    def create(self, request):
        subject = request.data.get('subject')
        if not subject:
            return Response("请传入课题参数", status=400)

        student = request.user.student
        subs = Subject.objects.filter(id=subject)
        if not subs.exists():
            return Response("该课题不存在", status=400)

        sub = subs[0]

        if sub.select_student:
            return Response("该课题已经有人选择,请选择其他课题", status=400)

        query_set = ApplySubject.objects.filter(student_id=student.id)
        if query_set.exists():
            latest_apply = query_set.order_by('-apply_time')[0]
            if latest_apply.apply_result == 0:
                return Response("你已经申请了课题,课题编号: {},请等待老师审核!".format(latest_apply.subject_id), status=400)
            elif latest_apply.apply_result == 1:
                return Response("你已经选择了课题!课题编号: {}".format(latest_apply.subject_id), status=400)

        query_set = ApplySubject.objects.filter(subject_id=sub.id)
        if query_set.exists():
            latest_apply = query_set.order_by('-apply_time')[0]
            if latest_apply.apply_result in [0, 1]:
                return Response("该课题已经有人申请, 请申请其他课题", status=400)

        data = {
            'subject': sub.id,
            'student': student.id,
            'apply_time': datetime.datetime.now(),
            'apply_result': 0
        }
        ser = ApplySubjectSerializer(data=data)
        if not ser.is_valid():
            print(ser.errors)
            return Response("Error", status=400)

        ser.save()
        return Response({'data': ser.data, 'msg': "选题成功!请等待老师审核"})


@api_view(["GET"])
def my_subject(request):
    """
    学生功能：我的课题
    """
    student = request.user.student

    select_subject = None
    if hasattr(student, 'select_student'):
        ser = SubjectSerializer(instance=student.select_student)
        select_subject = ser.data

    apply_subject = None
    apply = student.applysubject_set.all()
    if apply.exists():
        app = apply.order_by('-apply_time')[0]
        if app.apply_result == 0:
            ser = SubjectSerializer(instance=app.subject)
            apply_subject = ser.data

    response = {
        'select_subject': select_subject,
        'apply_subject': apply_subject
    }

    return Response(response)


class ApprovalApplicationViewSet(ViewSet):
    """
    教师功能: 审批学生选题申请
    """
    def list(self, request):
        query_set = ApplySubject.objects.filter(apply_result__in=[0, 1]).order_by('apply_result', '-apply_time')
        ser = ApplySubjectSerializer(instance=query_set, many=True)
        res_data = PendingSubjectViewSet.pagination(ser.data, request)

        return Response(res_data)

    def partial_update(self, request, pk=None):
        data = request.data
        apply_result = int(data.get('apply_result', 0))
        if not pk:
            return Response("为传入申请参数")

        apps = ApplySubject.objects.filter(pk=pk)
        if not apps.exists():
            return Response("该申请不存在")

        app = apps[0]
        ser = ApplySubjectSerializer(instance=app, data=data)

        if not ser.is_valid():
            return Response({'error': ser.errors}, status=400)

        if apply_result == 1:
            app.subject.select_student_id = app.student_id
            app.subject.save()
        ser.save()
        return Response(ser.data)


class SubjectViewSet(ViewSet):
    """
    通用功能
    """

    @action(detail=False)
    def selected_subject(self, request):
        """
        已经被选择的课题列表
        教师功能: 毕业设计过程---使用
        """
        user = request.user
        if hasattr(user, 'teacher'):
            query_set = Subject.objects.filter(review_result=1, select_student__isnull=False,
                                               questioner_id=user.teacher.id)
        else:
            query_set = Subject.objects.filter(review_result=1, select_student__isnull=False)

        ser = SubjectInfoSerializer(instance=query_set, many=True)
        res_data = PendingSubjectViewSet.pagination(ser.data, request)
        return Response(res_data)


class TaskBookViewSet(ViewSet):
    """
    通用功能:
        - 教师: 填写 + 查看 + 修改
        - 管理员: 审核
        - 学生: 查看
    """
    def retrieve(self, request, pk=None):
        if not pk:
            return Response({'msg': "请传入任务书参数"}, status=400)

        query_set = TaskBook.objects.filter(pk=pk)
        if not query_set.exists():
            return Response({'msg': "该任务书不存在"}, status=400)

        ser = TaskBookSerializer(instance=query_set[0])

        return Response({'data': ser.data, 'msg': '获取任务书成功'})

    def create(self, request):
        data = request.data
        data['release_time'] = datetime.datetime.now()
        ser = TaskBookSerializer(data=data)

        if not ser.is_valid():
            return Response({'msg': "数据不合法", 'error': ser.errors}, status=400)

        ser.save()
        return Response({'data': ser.data, 'msg': "ok"})

    def update(self, request, pk=None):
        """
        教师功能： 修改任务书（整体修改)
        """
        if not pk:
            return Response({"msg": "未传入任务书参数"}, status=400)

        query_set = TaskBook.objects.filter(pk=pk)
        if not query_set.exists():
            return Response({'msg': "该任务书不存在"}, status=400)

        data = request.data
        data['reviewer'] = None
        data['review_result'] = 0
        data['review_time'] = None

        ser = TaskBookSerializer(instance=query_set[0], data=data)
        if not ser.is_valid():
            return Response({'msg': "数据不合法", 'error': ser.errors}, status=400)

        ser.save()
        return Response({'data': ser.data, 'msg': "修改任务书成功"})

    def partial_update(self, request, pk=None):
        """
        管理员功能： 部分修改任务书（即，填写reviewer, review_result, review_time）
        """
        if not pk:
            return Response({"msg": "未传入任务书参数"}, status=400)

        query_set = TaskBook.objects.filter(pk=pk)
        if not query_set.exists():
            return Response({'msg': "该任务书不存在"}, status=400)

        data = request.data
        data['reviewer'] = request.user.administrator.id
        data['review_time'] = datetime.datetime.now()

        ser = TaskBookSerializer(instance=query_set[0], data=data, partial=True)
        if not ser.is_valid():
            return Response({'msg': "数据不合法", 'error': ser.errors}, status=400)

        ser.save()
        return Response({'data': ser.data, 'msg': "审核任务书成功"})
