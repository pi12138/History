from rest_framework import serializers
from . import models
from apps.article.models import Article
import json


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        fields = ('id', 'email', 'content', 'pub_date', 'article')
        extra_kwargs = {
            # 'email': {'read_only': True}
            'pub_date': {'format': '%Y-%m-%d %H:%M:%S'}
        }

