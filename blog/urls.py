from django.urls import path
from . import views


urlpatterns = [
    path('create_post/', views.PostCreate.as_view()),
    path('tag/<str:slug>/', views.tag_page),
    path('category/<str:slug>/', views.category_page),
    path('<int:pk>/', views.post_detail),
    path('', views.post_list),
       
]
