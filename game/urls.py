from django.urls import path
from . import views
from users.views import LoginView

urlpatterns = [
    path('', views.index, name='index'),
    path('reisgids/', views.reisgids, name='reisgids'),
    path('log-in/', LoginView.as_view(), name='log-in'),
    path('teams/', views.TeamListView.as_view(), name='teams'),
    path('questions/', views.QuestionsListView.as_view(), name='question-list'),
    path('questions/correct/', views.correctanswer, name='correct-answer'),
    path('questions/joker/', views.joker, name='joker'),
    path('questions/create/', views.QuestionCreate.as_view(), name='question-create'),
    path('questions/<uuid:pk>', views.question_page, name='question-page'),
    path('questions/<uuid:pk>/update/', views.QuestionUpdate.as_view(), name='question-update'),
    path('questions/<uuid:pk>/delete/', views.QuestionDelete.as_view(), name='question-delete'),
    path('questions/<uuid:pk>/answer/', views.AnswerView.as_view(), name='question-answer-view'),
]
