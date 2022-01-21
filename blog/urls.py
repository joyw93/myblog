from django.urls import path
from . import views


urlpatterns = [
    path('category/<str:slug>/', views.category_page),
    path('<int:pk>/', views.post_detail),
    path('', views.post_list),
       
]
