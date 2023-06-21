from django.shortcuts import render
from . import models, serializers
from rest_framework import viewsets 
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view, action
from apps.article.models import Article
# Create your views here.


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    @action(methods=['get'], detail=False)
    def get_comments_from_article(self, request, *args, **kwargs):
        """通过文章获取该文章的评论"""
        article_id = request.query_params.get('article_id', "")
        if not article_id:
            return Response("未传入文章ID")

        comments = self.get_queryset().filter(article_id=article_id).order_by('-pub_date')
        ser = serializers.CommentSerializer(instance=comments, many=True)

        return Response(ser.data)


@api_view()
def get_article_info_from_comment(request):
    """通过评论，获取被评论的文章信息"""
    # comments = models.Comment.objects.all().select_related('article')
    comments = models.Comment.objects.all().prefetch_related('article')

    article_list = []
    for com in comments:
        article_info = {}
        article_info['title'] = com.article.title
        article_info['category'] = com.article.category
        article_list.append(article_info) 

    return Response(article_list)       


class NewViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()

    def get_serializer_class(self):
        return serializers.CommentSerializer

