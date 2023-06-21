from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request

from blog.models import Article, Comment
from blog.rest.serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer
from blog.helpers import getAddrFromIP

import datetime


class ArticleViewSet(viewsets.ViewSet):
    """
    文章视图
    """

    def list(self, request):
        articles = Article.objects.all().order_by('-create_time')
        ser = ArticleListSerializer(instance=articles, many=True)

        return Response(ser.data)

    def retrieve(self, request, pk=None):
        if not pk:
            return Response({'msg': '为传入文章信息'}, status=400)

        articles = Article.objects.filter(id=pk)
        if not articles.exists():
            return Response({'msg': '文章不存在'}, status=400)

        ser = ArticleSerializer(instance=articles[0])
        return Response(ser.data)


class CommentViewSet(viewsets.ViewSet):
    """
    评论视图
    """
    def list(self, request):
        article_id = request.query_params.get('articleId')

        comments = Comment.objects.filter(article_id=article_id).order_by('-create_time')
        ser = CommentSerializer(instance=comments, many=True)

        return Response(ser.data)

    def create(self, request):
        data = request.data
        ip = request._request.META.get('REMOTE_ADDR')
        code, ip_address = getAddrFromIP(ip)

        data['user_ip'] = ip
        data['user_address'] = ip_address if code == 0 else ""
        data['create_time'] = datetime.datetime.now()

        ser = CommentSerializer(data=data)
        if not ser.is_valid():
            return Response({'error': ser.errors, 'msg': '数据不合法'}, status=400)

        ser.save()
        return Response(ser.data)
