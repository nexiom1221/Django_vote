from django.urls import path
from . import views

from .views import *

app_name = 'polls'



urlpatterns = [
    path('', views.index, name='index'), # /polls/
    path('<int:question_id>/', views.detail, name='detail'), # /polls/5/
    path('<int:question_id>/results/', views.results, name='results'), # /polls/5/results/
    path('<int:question_id>/vote/', views.vote, name='vote'), # /polls/5/vote/
    path('create/', views.create, name='create'), # /polls/create/
    path('<int:question_id>/modify/', views.modify, name='modify'), # /polls/5/modify
    path('<int:question_id>/delete/', views.delete, name='delete') # /polls/5/delete

]