from rest_framework.decorators import api_view
from rest_framework.response import Response
from main.serializers import *
from main.models import News, Category, Tag
from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


class TagModelViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = 3
    lookup_field = 'id'


class CategoryLIstApiView(ListAPIView, CreateAPIView):  # You can also use ListCreateAPIView, it can list and create too
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination


class CategoryDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


@api_view(['GET', 'POST'])
def news_list_api_view(request):
    if request.method == 'GET':
        search = request.query_params.get('search', '')
        # 1.Get list of news
        news = News.objects.select_related('category').prefetch_related('tags', 'news_comments').\
            filter(title__icontains=search)
        # 2.Convert list of news to list of dictionary
        data = NewsSerializer(instance=news, many=True).data
        # 3. Return dictionary as JSON
        return Response(data=data)

    elif request.method == 'POST':
        # Step0. Validation
        serializer = NewsValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=400, data=serializer.errors)
        # Step1. Get data from body
        title = serializer.validated_data.get('title')
        text = request.data.get('text')
        amount = request.data.get('amount')
        is_active = serializer.validated_data.get('is_active')
        category_id = request.data.get('category_id')
        tags = request.data.get('tags')
        # Step2. Create news by this data
        news = News.objects.create(
            title=title, text=text, view_amount=amount, is_active=is_active, category_id=category_id,
        )
        news.tags.set(tags)
        news.save()
        # Step3. Return created news
        return Response(data=NewsSerializer(news).data)


@api_view(['GET', 'POST', 'DELETE'])
def news_detail_api_view(request, news_id):
    try:
        news = News.objects.get(id=news_id)
    except News.DoesNotExist:
        return Response(data={"message: 'News object doesn't exists'"},
                        status=404)
    if request.method == 'GET':
        data = NewsSerializer(instance=news, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        # Validate ver.2
        serializer = NewsValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        news.title = request.data.get('title')
        news.text = request.data.get('text')
        news.amount = request.data.get('amount')
        news.is_active = request.data.get('is_active')
        news.category_id = request.data.get('category_id')
        news.tags.set(request.data.get('tags'))
        news.save()
        return Response(data=NewsSerializer(news).data)
    else:
        news.delete()
        return Response(status=204)
