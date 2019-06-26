from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('questions/', views.QuestionListView.as_view(), name='questions'),
    path('answers/', views.AnswerListView.as_view(), name='answers'),
    path('question/<int:pk>', views.QuestionDetailView.as_view(), name='question-detail'),

]