from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.home, name='index'),
    path('home', views.home, name='home'),
    path('article/<slug:uuid>', views.article, name='article'),
    path('comment/<slug:uuid>', views.new_comment, name='comment'),
]