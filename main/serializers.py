from rest_framework import serializers
from main.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = 'author text'.split()


class NewsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)
    category_name = serializers.SerializerMethodField()
    news_comments = CommentSerializer(many=True)

    class Meta:
        model = News
        fields = 'id category tags title text is_active category_name category_str'.split()
    # 1 version
    # def get_category_name(self, news):
    #     if news.category:
    #         return news.category.name
    #     return None
