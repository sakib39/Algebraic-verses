from django.urls import path
from .views import category_list, problem_list
from . import views

urlpatterns = [
    path('', category_list, name='category_list'),
    path('<int:category_id>/', problem_list, name='problem_list'),
    path('categories/<int:category_id>/', views.problem_list, name='problem_list'),
    path('<int:problem_id>/answer/', views.problem_answer, name='problem_answer'),
]
