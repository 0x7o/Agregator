from rest_framework import serializers
from . import models


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = ["url", "title", "text", "image", "friendly_url"]
