from .models import Article, ArticleCategory
from rest_framework import serializers
from apps.comment.models import Comment
from apps.comment.serializers import CommentSerializer


class ArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'category', 'category_name', 'pub_date', 'update_time', 'content',
        'article_read_number', 'article_comment_number')
        extra_kwargs = {
            'category': {'write_only': True},
            'update_time': {'format': "%Y-%m-%d %H:%M:%S"},
            'pub_date': {'format': '%Y-%m-%d %H:%M:%S'},
        }


class IndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'category_name', 'update_time', 'id')
        extra_kwargs = {
            'title': {'read_only': True},
            'update_time': {'format': '%Y-%m-%d %H:%M:%S'}    
        }


class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCategory
        fields = "__all__"


class ArticleSer(serializers.ModelSerializer):
    # 导数据专用
    class Meta:
        model = Article
        fields = "__all__"