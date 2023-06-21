# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserIP, UserInterviewInfo
from .serializers import UserIPSerializer
from apps.article.models import Article

from collections import Counter
import datetime
# Create your views here.


@api_view(http_method_names=['GET'])
def interview_count(request):
    """
    访问数量统计,返回网站访问总数量，访问网站的IP总数量
    """
    users = UserIP.objects.all()
    
    if not users.exists():
        return Response({'count': 0})

    count = sum([user.count for user in users])

    return Response({'count': count, "IP_count": users.count()})

@api_view(http_method_names=['GET'])
def one_day_visits(request):
    """
    一天的访问量
    """
    date = request.query_params.get('date')

    if not date:
        # 未传入时间，默认为当前时间
        date = datetime.datetime.now()
        date = date.strftime('%Y-%m-%d')
    year, month, day = date.split('-')
    users = UserInterviewInfo.objects.filter(interview_time__year=year, interview_time__month=month, interview_time__day=day)
    ip_count_set = set(users.values_list('ip', flat=True))

    return Response({'count': users.count(), "IP_count": len(ip_count_set)})


@api_view(http_method_names=['GET'])
def article_read_count(request):
    """
    文章的访问数量
    """
    article = request.query_params.get('article', "")

    if not article:
        return Response("为传入文章ID")

    path = "/api/blogv2/articles/{}/".format(article)

    users = UserInterviewInfo.objects.filter(interview_url=path)
    
    return Response({'count': users.count()})


@api_view(http_method_names=['GET'])
def today_read_article(request):
    """
    今天被访问的文章
    """
    today = datetime.datetime.now()
    year, month, day = today.strftime('%Y-%m-%d').split('-')
    path = r'/api/blogv2/articles/[0-9]*/'

    users = UserInterviewInfo.objects.filter(interview_time__year=year, interview_time__month=month, interview_time__day=day)
    urls = users.filter(interview_url__regex=path).values_list('interview_url', flat=True)

    # url_dict = dict()
    # for url in urls:
    #     if url in url_dict.keys():
    #         url_dict[url] += 1
    #     else:
    #         url_dict[url] = 1

    # 使用Counter()也可以实现上述功能
    url_dict = Counter(urls)

    url_list = list()
    for k, v in url_dict.items():
        res = dict()
        res['url'] = k
        res['count'] = v
        res['id'] = k.split('/')[-2]
        art = Article.objects.filter(pk=res['id']).values_list('title', flat=True)
        res['title'] = art[0] if art else ""

        url_list.append(res)

    return Response(url_list)


@api_view(http_method_names=['GET'])
def hot_ip(request):
    """
    访问次数最多的IP
    """
    ip = UserIP.objects.all().order_by('-count')
    num = ip.count()

    if num > 5:
        num = 5

    ser = UserIPSerializer(instance=ip[:num], many=True)

    return Response(ser.data)