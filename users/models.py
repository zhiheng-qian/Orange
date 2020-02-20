from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
	# name = models.CharField(max_length=100,unique=False)
	# email = models.EmailField(max_length=256,unique=False)
	# password = models.CharField(max_length=100,blank=True)
	isDeveloper = models.BooleanField(default=False)
	
	def created_game(self, game):
		return game.developer == self.username
	def __str__(self):
		return self.username
	