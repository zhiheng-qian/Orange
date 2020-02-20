from django.contrib import admin
from .models import Game, GameCategory

#add game_category from /admin
admin.site.register(Game)
admin.site.register(GameCategory)
