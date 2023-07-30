from django.contrib import admin
from django.urls import path, include
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/news', include('main.urls')),
    path('api/v1/news/<int:news_id>/', include('main.urls')),
    path('api/v1/users/', include('users.urls'))
]
