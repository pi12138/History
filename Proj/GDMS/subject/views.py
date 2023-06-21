from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator
# Create your views here.
from user.mixins import LoginRequiredMixin
from .models import Subject
from subject.rest.serializers import SubjectSerializer

import json
import datetime


@method_decorator(csrf_exempt, name='dispatch')
class DeclareSubject(LoginRequiredMixin, View):
    """
    教师功能：申报课题
    """

    def get(self, request):
        page = int(request.GET.get('page', 1))
        teacher = request.user.teacher

        query_set = Subject.objects.filter(questioner=teacher).order_by('-review_result', '-declare_time')
        pagi = Paginator(query_set, 10)
        num_pages = pagi.num_pages

        if page > num_pages:
            page = num_pages

        pa = pagi.page(page)

        context = {
            'page': pa
        }

        return render(request, 'declare_subject.html', context)

    def post(self, request):
        body = request.body.decode()
        data = json.loads(body)

        subject_name = data.get('subjectName')
        number_of_people = data.get('number')
        subject_description = data.get('subjectDesc')
        expected_goal = data.get('expectGoal')
        require = data.get('require')
        required_conditions = data.get('requiredConditions')
        references = data.get('references')
        declare_time = datetime.datetime.now()
        arg_list = [subject_name, number_of_people, subject_description,
                    expected_goal, require, required_conditions, references]

        if not all(arg_list):
            return JsonResponse("课题参数不全！", safe=False, status=400)

        query = Subject.objects.filter(subject_name=subject_name)
        if query.exists():
            return JsonResponse("该课题已经存在，请换用其他课题！", safe=False, status=400)

        Subject.objects.create(
            subject_name=subject_name,
            questioner=request.user.teacher,
            number_of_people=number_of_people,
            subject_description=subject_description,
            expected_goal=expected_goal,
            require=require,
            required_conditions=required_conditions,
            references=references,
            declare_time=declare_time,

        )

        return JsonResponse("申报课题成功，请等待审核！", safe=False, status=200)


@method_decorator(csrf_exempt, 'dispatch')
class AlterSubject(LoginRequiredMixin, View):
    """
    教师功能：修改单个课题
    """
    def get(self, request):
        subject_id = request.GET.get('subject_id')

        if not subject_id:
            return JsonResponse("为传入课题", safe=False, status=400)

        sub = Subject.objects.filter(id=subject_id)
        if not sub.exists():
            return JsonResponse("该课题不存在", safe=False, status=400)

        ser = SubjectSerializer(instance=sub[0])

        return JsonResponse(ser.data, status=200)

    def post(self, request):
        body = request.body.decode()
        data = json.loads(body)
        subject_id = data.get('subject_id')
        data['declare_time'] = datetime.datetime.now()

        if data['review_result_number'] == 2:
            data['review_result_number'] = 0
            data['review_reason'] = ""
            data['reviewer'] = None

        query_set = Subject.objects.filter(id=subject_id)
        if not query_set.exists():
            return JsonResponse({'msg': "该课题不存在"}, safe=False, status=400)

        subject = query_set[0]
        ser = SubjectSerializer(instance=subject, data=data)

        if not ser.is_valid():
            return JsonResponse({'msg': "修改失败", 'data': ser.errors}, safe=False, status=400)

        ser.save()
        return JsonResponse({'msg': "修改成功", 'data': ser.data}, safe=False, status=200)


class ApprovalSubject(LoginRequiredMixin, View):
    """
    管理员功能：审核课题
    """

    def get(self, request):
        return render(request, 'approval_subject.html')

    def post(self, request):
        pass


class PassedSubject(LoginRequiredMixin, View):
    """
    管理员功能：审核通过课题
    """
    def get(self, request):
        return render(request, 'passed_subject.html')


class SelectSubject(LoginRequiredMixin, View):
    """
    学生功能： 选择课题
    """
    def get(self, request):
        return render(request, 'select_subject.html')


class ApprovalApplication(LoginRequiredMixin, View):
    """
    老师功能： 审批学生的选题申请
    """
    def get(self, request):
        return render(request, 'approval_application.html')


