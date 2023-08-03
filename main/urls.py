from . import views
from django.urls import path


urlpatterns = [
    path('', views.news_list_api_view),
    path('<int:id>/', views.news_detail_api_view),
    path('categories/', views.CategoryLIstApiView.as_view()),
    path('categories/<int:id>', views.CategoryDetailApiView.as_view()),
    path('tags/', views.TagModelViewSet.as_view({
        'get': 'list', 'post': 'create'
    })),
    path('tags/<int:id>', views.TagModelViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
    }))
]
