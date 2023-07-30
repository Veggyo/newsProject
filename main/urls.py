from . import views
from django.urls import path


urlpatterns = [
    path('', views.news_list_api_view),
    path('<int:id>/', views.news_detail_api_view),
]
