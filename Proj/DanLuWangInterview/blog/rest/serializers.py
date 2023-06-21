from rest_framework import serializers

from blog.models import Article, Comment


class ArticleListSerializer(serializers.ModelSerializer):
    """文章列表序列化器"""
    class Meta:
        model = Article
        fields = ('id', 'title', 'create_time')
        extra_kwargs = {
            'create_time': {'format': '%Y-%m-%d %H:%M:%S'}
        }


class ArticleSerializer(serializers.ModelSerializer):
    """单个文章序列化器"""
    class Meta:
        model = Article
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {
            'user_ip': {'write_only': True},
            'article': {'write_only': True},
            'create_time': {'format': '%Y-%m-%d %H:%M:%S'}
        }
