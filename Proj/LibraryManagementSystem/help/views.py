from django.shortcuts import render
from help.models import *
from django.http import HttpResponse
from user.views import get_time
from django.core.paginator import Paginator
# Create your views here.


def opinion_list(request, page_index):
    """意见列表"""
    user_name = request.session.get('user_account', None)

    if user_name is None:
        return render(request, 'login/login.html')
    else:

        feedback = FeedBackInfo.objects.all()

        # reversed(feedback)，目的是为了将列表反转，以便意见列表的消息是按时间顺序从新到旧,
        # reversed()返回一个迭代器
        feedback = list(reversed(feedback))

        # 分页
        paginator = Paginator(feedback, 2)
        if page_index == "":
            page_index = 1

        page_list = paginator.page(page_index)

        context = {
            "user_name": user_name,
            # "feedback": feedback,
            "page": page_list,
            "page_range": paginator.page_range,
        }
        return render(request, 'help/opinion_list.html', context)


def write_opinion(request):
    """保存写下的意见"""

    user_account = request.POST.get("user_name", None)

    if user_account is None:
        return render(request, "login/login.html")
    else:
        try:
            opinion_content = request.POST.get("opinion_content", None)

            feed = FeedBackInfo()
            feed.user_account = user_account
            feed.opinion_content = opinion_content
            feed.issuing_time = get_time()
            feed.save()

            context = {
                "save_result": "保存成功",
            }

            return render(request, "help/opinion_list.html", context)

        except Exception as e:
            return HttpResponse("write_opinion error:{}".format(e))


def guide(request):
    """使用指南"""
    return render(request, 'help/guide.html')

