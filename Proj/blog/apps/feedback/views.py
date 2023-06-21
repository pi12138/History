from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
# Create your views here.
from apps.feedback.models import FeedBack


# /feedback/list/
class FeedBackListView(View):
    """Blog留言列表"""
    def get(self, request):
        """显示留言列表"""
        try:
            feedback_list = FeedBack.objects.all().order_by('-pub_date')
        except Exception as e:
            return render(request, 'error.html', {'errmsg': '发生错误，错误原因{}'.format(e)})

        context = {
            'feedback_list': feedback_list,
        }

        return render(request, 'feedback/feedback.html', context)


# /feedback/add/
class FeedBackAddView(View):
    """添加留言"""
    def post(self, request):
        """添加留言到留言表"""
        email = request.POST.get('email')
        content = request.POST.get('content')

        if not all([email, content]):
            return JsonResponse({'res': 1, 'errmsg': "邮箱或者留言内容为空！"})

        try:
            feedback = FeedBack()
            feedback.email = email
            feedback.content = content
            feedback.save()
            return JsonResponse({'res': 0, 'message': '添加留言成功！'})
        except Exception as e:
            return JsonResponse({'res': 2, 'errmsg': e})
