from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reisgids/', views.reisgids, name='reisgids'),
    path('teams/', views.TeamListView.as_view(), name='teams'),
    path('questions/', views.QuestionsListView.as_view(), name='questions'),
    path('questions/correct/', views.correctanswer, name='correct_answer'),
    path('questions/correct/', views.joker, name='joker'),
    path('questions/create/', views.QuestionCreate.as_view(), name='question_create'),
    path('questions/<uuid:pk>', views.get_answer, name='question-detail-view'),
    path('questions/<uuid:pk>/update/', views.QuestionUpdate.as_view(), name='question-update'),
    path('questions/<uuid:pk>/delete/', views.QuestionDelete.as_view(), name='question-delete'),
    path('questions/<uuid:pk>/answer/', views.QuestionDetailAnswerView.as_view(), name='question-answer-view'),
]
