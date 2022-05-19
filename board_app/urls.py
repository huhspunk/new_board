from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'board'

urlpatterns = [
    path('', views.index, name='index'),
    path('post', views.post, name='post'),
    path('post/<int:pk>', views.detail, name='detail'),
    path('post/delete/<int:pk>', csrf_exempt(views.delete), name='delete'),
    path('<int:pk>/post/comment/write/', views.comment_write_view, name='comment_write'),
]
