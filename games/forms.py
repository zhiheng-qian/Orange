from django import forms
from games.models import Game

#the form format for developer creating games
class GameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ['name', 'price', 'content', 'category', 'description',
                  'discount', 'logo']