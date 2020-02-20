from django.conf.urls import include, url, re_path
from django.urls import path
from games import views

#actions for operating games
urlpatterns = [
    path('game_form', views.game_create, name="game_create"),
    path('game_form/<int:id>', views.game_edit, name="game_edit"),
    path('game_delete/<int:id>', views.game_delete, name="game_delete"),
    re_path(r'^(?P<game_id>\d+)/play', views.play_game, name='game-play'),
]
