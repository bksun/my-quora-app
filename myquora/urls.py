from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('question/add/', views.QuestionCreate.as_view(), name='question-add'),
    path('questions/', views.QuestionListView.as_view(), name='questions'),
    path('answers/', views.AnswerListView.as_view(), name='answers'),
    path('question/<int:pk>', views.QuestionDetailView.as_view(), name='question-detail'),
    path('question/<int:pk>/answer/', views.AnswerCreate.as_view(), name='answer-add'),
    path('question/<int:pk>/update/', views.UpdateQuestion.as_view(), name='question-update'),
    path('answer/<int:pk>/update/', views.UpdateAnswer.as_view(), name='answer-update'),
    path('answer/<int:pk>/comment/', views.CommentCreate.as_view(), name='comment-add'),
    path('answer/upvote/<int:pk>', views.UpvoteCreate.as_view(), name='answer-upvote'),
    path('answer/downvote/<int:pk>', views.DownvoteCreate.as_view(), name='answer-downvote'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/add/', views.AuthorCreate.as_view(), name='author-add'),
    path('author/<int:pk>/', views.AuthorUpdate.as_view(), name='author-update')
]
