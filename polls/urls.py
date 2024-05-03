from django.urls import path, re_path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # ex: /polls/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # re_path(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('results/<int:pk>/', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    path('vote/<int:question_id>/', views.vote, name='vote'),
]