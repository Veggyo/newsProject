from rest_framework import serializers
from main.models import *
from rest_framework.exceptions import ValidationError


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


class NewsValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=10, max_length=100)
    text = serializers.CharField(required=False, default='empty text')
    amount = serializers.IntegerField(required=True)
    is_active = serializers.BooleanField()
    category_id = serializers.IntegerField(min_value=1)
    tags = serializers.ListField(child=serializers.IntegerField(min_value=1))

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category does not exists')
        return category_id
