from django.urls import path
from django.conf.urls import url

from . import views, actions
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',  views.index, name='index'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^search/$', views.SearchPlayerView.as_view(), name='search'),
    path('competition/<competitionId>', views.competitionview, name="competition"),
    path('news/<newsId>', views.news, name="news"),
    path('team/<teamId>', views.teamview, name="team"),
    path('player/<playerId>', views.playerview, name="player"),
    path("cssexample", views.cssexample, name="cssexample"),
    path("ajax/<ajaxAction>", views.ajax, name="ajax"),
]