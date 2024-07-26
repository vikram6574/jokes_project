from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('joke/', views.get_joke, name='get_joke'),
    path('categories/', views.get_categories, name='get_categories'),
]
