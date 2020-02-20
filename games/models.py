from django.contrib.postgres.fields import ArrayField
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    int_list_validator)
from django.db import models

# from jsonfield import JSONField
from django.contrib.postgres.fields import JSONField

from users.models import CustomUser
from django.utils import timezone

#foreignkey about GameCategory
class GameCategory(models.Model):
    name = models.fields.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

#the game modle
class Game(models.Model):
	name = models.CharField(max_length=100, unique=True)
	developer = models.CharField(max_length=254) #people who game belong to
	price = models.PositiveIntegerField()
	content = models.URLField(unique=True) #url
	uploadDate = models.DateTimeField(auto_now=True)
	description = models.TextField(null=True, blank=True)
	category = models.ForeignKey(GameCategory, on_delete=models.DO_NOTHING)
	sales = models.PositiveIntegerField(default=0)
	globalScore = models.PositiveIntegerField(null=True)
	gameStates = models.TextField(max_length=1000, null=True)
	users = models.ManyToManyField(CustomUser, related_name='games', blank=True) #manytomany model
	reviews = models.TextField(null=True)
	discount = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True,
								   validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
	logo = models.ImageField(upload_to="./images/", default="images/site_logo.jpg", blank=True)
	
	class Meta:
		#order by sales quantity
		ordering = ['-sales']

	def __str__(self):
		return self.name

	#filter top score
	def user_best_score(self, user):
		high_score = self.gamescore_set.filter(player=user).order_by('-score').first()
		high_score_value = high_score.score if high_score is not None else None
		return high_score_value

	def user_last_state(self, user):
		return self.gamestate_set.filter(player=user).order_by('-timestamp').first()

#model for score of each game
class GameScore(models.Model):
    player = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING)
    score = models.fields.PositiveIntegerField(null=True)
    timestamp = models.DateTimeField(auto_now=True)

#keep state of each game
class GameState(models.Model):
    player = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING)
    state_data = JSONField()
    timestamp = models.DateTimeField(auto_now=True)