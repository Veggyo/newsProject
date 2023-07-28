from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/news', views.news_list_api_view),
    path('api/v1/news/<int:news_id>/', views.news_detail_view)
]
