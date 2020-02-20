from django.conf.urls import include, url
from django.urls import path
from . import views

urlpatterns = [
    path('games', views.games, name="games"),
    path('games/<int:id>', views.game_detail, name="game"),
    path('', views.games),
    path('home', views.games, name="home"),
    path('games/<int:id>/info', views.game_info, name="game_info"),
    path('games/<int:id>/state', views.game_api, name="game_api"),
    path('games/<int:id>/info/logo', views.game_logo, name="game_logo"),
    path('games/uplad_fail', views.game_upload_fail, name="game_upload_fail")
]   
