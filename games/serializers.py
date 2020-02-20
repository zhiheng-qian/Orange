from rest_framework import serializers
from .models import Game

#Turn the game into a saveable format
class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('name', 'developer', 'price', 'content',
                  'uploadDate', 'description', 'category', 'sales',
                  'globalScore', 'gameStates', 'users', 'reviews', 'discount',)

        def create(self, validated_data):
            return Game.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.discount = validated_data.get('discount', instance.discount)
            instance.content = validated_data.get('content', instance.content)
            instance.description = validated_data.get('description', instance.description)
            instance.save()
            return instance
